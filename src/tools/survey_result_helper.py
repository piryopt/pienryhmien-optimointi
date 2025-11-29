from flask_babel import gettext
from src.entities.group import Group
from src.entities.student import Student
from src.services.survey_service import survey_service
from src.services.user_service import user_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.tools.rankings_converter import convert_to_list, convert_to_int_list
import src.algorithms.hungarian as h
import src.algorithms.weights as w
import copy
from flask import current_app


def build_output(survey_id):
    """
    Build results structure for a regular (single-stage) survey.
    Returns the same tuple that hungarian_results returns or None if no answers.
    """
    user_rankings = survey_service.fetch_survey_responses(survey_id)
    if not user_rankings:
        return None
    survey_answers_amount = len(user_rankings)

    # Ensure groups meet min_size constraints by adding empty choice(s) if needed
    answers_less_than_min_size = survey_choices_service.check_answers_less_than_min_size(survey_id, survey_answers_amount)
    if answers_less_than_min_size:
        survey_choices_service.add_empty_survey_choice(survey_id, survey_answers_amount)

    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    groups_dict = convert_choices_groups(survey_choices)
    students_dict = convert_users_students(user_rankings)

    output_data = hungarian_results(survey_id, user_rankings, groups_dict, students_dict, survey_choices)
    return output_data


def build_multistage_output(survey_id):
    """
    Build results structure for a multistage survey.
    Returns a list of stage_result dicts (same shape as before).
    """
    multistage_user_rankings = survey_service.fetch_survey_responses_grouped_by_stage(survey_id)
    if not multistage_user_rankings:
        return None

    stages = survey_service.get_all_survey_stages(survey_id)

    participation_limits, participation_limit_group_names = get_participation_limits(survey_id, stages)
    participation_counts = {}
    output_data = []

    for stage in stages:
        survey_choices = survey_choices_service.get_list_of_stage_survey_choices(survey_id, stage.stage)
        groups_dict = convert_choices_groups(survey_choices)
        students_dict, absent_students_dict = convert_users_students(multistage_user_rankings.get(stage.stage, []), True)

        prune_students_for_limits(students_dict, participation_limit_group_names, participation_limits, participation_counts)

        if students_dict == {}:
            # Fix bug where app crashes when all students are absent
            dropped_group_names = [group.name for group in groups_dict.values()]
            stage_output_data = [[], 0, [], dropped_group_names, [], []]
        else:
            stage_output_data = hungarian_results(
                survey_id, multistage_user_rankings.get(stage.stage, []), groups_dict, students_dict, survey_choices
            )
            update_participation_counts(stage_output_data[0], participation_limit_group_names, participation_counts)

        absent_students_list = absent_students_output(absent_students_dict)
        results = stage_output_data[0] + absent_students_list if absent_students_list != [] else stage_output_data[0]

        stage_result = {
            "stage": stage.stage,
            "results": results,
            "happinessData": stage_output_data[2],
            "happiness": stage_output_data[1],
            "infos": stage_output_data[4],
            "additionalInfoKeys": stage_output_data[5],
            "droppedGroups": stage_output_data[3],
        }
        output_data.append(stage_result)

    return output_data


def hungarian_results(survey_id, user_rankings, groups_dict, students_dict, survey_choices):
    """
    Run the hungarian algorithm until there is no violation for the min_size portion

    args:
        survey_id: The id of the survey
        user_rankings: The rankings for the survey in question
        groups_dict: A dict containing survey choices which have been converted into group entities. Needed for the hungarian algorithm
        students_dict: A dict containing users which have been converted into students entities. Needed for the hungarian algorithm
        survey_choices: The choices of the survey in question

    returns:
        The output data from the algorithm along with happiness average, happiness results, dropped groups and additional infos
    """
    survey_answers_amount = len(user_rankings)
    dropped_groups_id = []

    output_data, unranked_or_rejected, original_students_dict = run_hungarian(
        survey_id, survey_answers_amount, groups_dict, students_dict, dropped_groups_id
    )
    additional_infos, cinfos = get_additional_infos(survey_choices)

    happiness_sum, happiness_results, valid_count = get_happiness_data(output_data, original_students_dict)
    happiness_avg = (happiness_sum / valid_count) if valid_count > 0 else 1

    infos = survey_choices_service.get_choice_additional_infos(survey_choices[0].id)

    additional_info_keys = [list(i.keys()) for i in infos]
    infos = [list(i.values()) for i in infos]

    happiness_results_list = []
    for k, v in happiness_results.items():
        if v > 0:
            if k == gettext("Kielletty"):
                k = gettext("Kiellettyyn")
                msg = gettext(" valintaan sijoitetut käyttäjät: ")
            elif k == gettext("Ei järjestetty"):
                k = gettext("Ei järjestettyyn")
                msg = gettext(" valintaan sijoitetut käyttäjät: ")
            else:
                msg = ". valintaansa sijoitetut käyttäjät: "
            happiness_results_list.append((k, msg, v))

    happiness_results_list.sort(key=happiness_sort_key)
    dropped_groups = dropped_group_names(dropped_groups_id)

    output_data = (output_data, happiness_avg, happiness_results_list, dropped_groups, infos, additional_info_keys)
    return output_data


def run_hungarian(survey_id, survey_answers_amount, groups_dict, students_dict, dropped_groups_id):
    """
    Run the hungarian algorithm until no violation.

    args:
        survey_id: The id of the survey
        survey_answers_amount: The amount of answers for the survey in question
        groups_dict: A dict containing survey choices which have been converted into group entities. Needed for the hungarian algorithm
        students_dict: A dict containing users which have been converted into students entities. Needed for the hungarian algorithm
        dropped_groups_id: A list to which the ids of dropped groups will be appended

    returns:
        The output data from the hungarian algorithm when there are no violations
    """
    students_dict_original = copy.deepcopy(students_dict)

    loop = True
    while loop:
        seats = get_seats(groups_dict)

        # If there are less seats than survey answers, add an empty group
        if seats < survey_answers_amount:
            empty_group_id = survey_choices_service.add_empty_survey_choice(survey_id, survey_answers_amount - seats)
            empty_group = survey_choices_service.get_survey_choice(empty_group_id)

            groups_dict[empty_group["id"]] = Group(
                empty_group["id"], empty_group["name"], empty_group["max_spaces"], empty_group["min_size"], empty_group["participation_limit"]
            )

        # Run the algotrithm with the groups that haven't been dropped
        weights = w.Weights(len(groups_dict), len(students_dict)).get_weights()
        sort = h.Hungarian(groups_dict, students_dict, weights)
        sort.run()
        output_data = sort.get_data()
        group_sizes = get_group_sizes(output_data, groups_dict)

        # Check if min_size is greater than group size. If not drop the group.
        # If the group is mandatory, try to fill it first by reassigning students from other groups.
        violation = False
        sorted_groups = [k for k, v in sorted(group_sizes.items(), key=lambda item: item[1])]
        for survey_choice_id in sorted_groups:
            # min_size = survey_choices_service.get_survey_choice_min_size(survey_choice_id)
            min_size = groups_dict[survey_choice_id].min_size
            # mandatory = survey_choices_service.get_survey_choice_mandatory(survey_choice_id)
            mandatory = groups_dict[survey_choice_id].mandatory

            if min_size > group_sizes[survey_choice_id]:
                violation = True
                if mandatory:
                    needed = min_size - group_sizes[survey_choice_id]
                    candidates = get_candidates(students_dict_original, survey_choice_id, output_data, group_sizes, needed)

                    #  Drop mandatory group when there are not enough students to fill all of the mandatory groups
                    if len(candidates) < needed:
                        drop_choice(groups_dict, students_dict, survey_choice_id)
                        dropped_groups_id.append(survey_choice_id)
                        break

                    # Reassign the best fitting candidates
                    candidates.sort(key=lambda c: rank(students_dict_original, c[1], survey_choice_id))
                    reassign_students(survey_choice_id, candidates, needed, students_dict, groups_dict, output_data, group_sizes)
                    group_sizes[survey_choice_id] = min_size
                    break
                else:
                    # Non-mandatory underfilled → drop it
                    drop_choice(groups_dict, students_dict, survey_choice_id)
                    dropped_groups_id.append(survey_choice_id)
                    break

        unranked_or_rejected = students_in_unranked_or_rejected_groups(output_data, students_dict_original)

        if not violation:
            return output_data, unranked_or_rejected, students_dict_original


def get_seats(groups_dict):
    """
    Get the amount of available seats in the remaining groups

    args:
        groups_dict: A dict containing survey choices which have been converted into group entities.
    """
    seats = 0
    for id, group in groups_dict.items():
        seats += group.size
    return seats


def get_group_sizes(output_data, groups_dict):
    """
    Count how many students each group has

    args:
        output_data: The current output data from the hungarian algorithm
        groups_dict: A dict containing survey choices which have been converted into group entities.
    """
    group_sizes = {}
    for id, group in groups_dict.items():
        group_sizes[id] = 0
    for [student_data, student_email, group_data] in output_data:
        group_id = group_data[0]
        group_sizes[group_id] += 1

    return group_sizes


def get_candidates(students_dict, survey_choice_id, output_data, group_sizes, needed):
    """
    Collect candidates for reassignment to a mandatory group.

    args:
        students_dict: A dict containing users which have been converted into students entities.
        survey_choice_id: The id of the mandatory group needing more students
        output_data: The current output data from the hungarian algorithm
        group_sizes: A dict mapping group IDs to their current sizes
        needed: The number of students needed to fill the mandatory group

    returns:
        A list of tuples (index in output_data, student_id, old_group_id) representing candidates for reassignment
    """
    # Collect candidates, Phase 1
    candidates = []
    students_in_mandatory_groups = []
    for i, entry in enumerate(output_data):
        student_info, email, group_info = entry
        student_id = student_info[0]
        assigned_group = group_info[0]

        # Skip students already in this mandatory group
        if assigned_group == survey_choice_id:
            continue

        if students_dict[student_id].not_available:
            continue

        # Skip students in other mandatory groups if they prefer their current mandatory group more
        if survey_choices_service.get_survey_choice_mandatory(assigned_group):
            current_group_rank = rank(students_dict, student_id, assigned_group)
            target_group_rank = rank(students_dict, student_id, survey_choice_id)
            current_group_min_size = survey_choices_service.get_survey_choice_min_size(assigned_group)

            if current_group_rank <= target_group_rank and group_sizes[assigned_group] <= current_group_min_size:
                students_in_mandatory_groups.append((i, student_id, assigned_group))
                continue

        candidates.append((i, student_id, assigned_group))

    # If not enough candidates, Phase 2: pull from other mandatory groups (respect min_size for mandatory groups)
    if len(candidates) < needed:
        for i, student_id, assigned_group in students_in_mandatory_groups:
            current_group_min_size = survey_choices_service.get_survey_choice_min_size(assigned_group)

            if group_sizes[assigned_group] <= current_group_min_size:
                continue

            candidates.append((i, student_id, assigned_group))

    return candidates


def rank(students_dict, student_id, target_group_id):
    """
    args:
        students_dict: A dict containing users which have been converted into students entities.
        student_id: The id of the student whose ranking we want to check
        target_group_id: The id of the group whose ranking we want to check

    Get the ranking index of a target group for a specific student.

    returns: The index of the target group in the student's selections or 999 if not found
    """
    selections = students_dict[student_id].selections
    rejections = students_dict[student_id].rejections

    if target_group_id in rejections:
        return 1000

    return selections.index(target_group_id) if target_group_id in selections else 999


def drop_choice(groups_dict, students_dict, dropped_choice_id):
    """
    Remove a choice from all relevant lists and dictionaries.

    args:
        groups_dict: A dict containing survey choices which have been converted into group entities.
        students_dict: A dict containing users which have been converted into students entities.
        dropped_choice_id: The id of the survey choice to be removed
    """
    groups_dict.pop(dropped_choice_id)
    for user_id, student in students_dict.items():
        if dropped_choice_id in student.selections:
            student.selections.remove(dropped_choice_id)
        if dropped_choice_id in student.rejections:
            student.rejections.remove(dropped_choice_id)


def reassign_students(target_group_id, candidates, amount, students_dict, groups_dict, output_data, group_sizes):
    """
    Reassign students to a group

    args:
        target_group_id: The id of the group to which students will be reassigned
        candidates: A list of tuples (index in output_data, student_id, old_group_id) representing students who can be reassigned
        students_dict: A dict containing users which have been converted into students entities.
        groups_dict: A dict containing survey choices which have been converted into group entities.
        output_data: The current output data from the hungarian algorithm
        group_sizes: A dict mapping group IDs to their current sizes
        amount: The number of students to reassign
    """
    for j in range(amount):
        idx, student_id, old_group = candidates[j]
        output_data[idx][2] = [target_group_id, groups_dict[target_group_id].name]  # overwrite group assignment
        group_sizes[old_group] -= 1
        group_sizes[target_group_id] += 1

        # Lock this student into the mandatory group so that the hungarian algorithm doesn't move them again
        students_dict[student_id].selections = [target_group_id]


def students_in_unranked_or_rejected_groups(output_data, students_dict):
    """
    Count how many students are in unranked or rejected groups

    args:
        output_data: The output data from the hungarian algorithm along with happiness average, happiness results, dropped groups and additional infos
    """
    return sum(
        1
        for result in output_data
        if ((result[2][0] in students_dict[result[0][0]].rejections) or (result[2][0] not in students_dict[result[0][0]].selections))
    )


def get_additional_infos(survey_choices):
    """
    Create a dict which contains choice's additional info as list

    args:
        survey_choices: The choices of the survey in question
    """
    additional_infos = {}
    for row in survey_choices:
        additional_infos[str(row.id)] = []

        cinfos = survey_choices_service.get_choice_additional_infos(row.id)
        for i in cinfos:
            additional_infos[str(row.id)].append(i["info_value"])

        mandatory = survey_choices_service.get_survey_choice_mandatory(row.id)
        min_size = survey_choices_service.get_survey_choice_min_size(row.id)
        if mandatory:
            additional_infos[str(row.id)].append(f"Minimikoko: {min_size}")

    return additional_infos, cinfos


def get_happiness_data(output_data, survey_id):
    """
    Extract happiness data from the output data.

    args:
        output_data: The output data from the hungarian algorithm along with happiness average, happiness results, dropped groups and additional infos
        survey_id: The id of the survey
    """
    students_dict = survey_id if isinstance(survey_id, dict) else None

    happiness_results = {}
    happiness_sum = 0
    valid_count = 0

    for results in output_data:
        user_id = results[0][0]
        choice_id = results[2][0]

        if students_dict and user_id in students_dict:
            ranking = students_dict[user_id].selections
            rejections = students_dict[user_id].rejections
        else:
            ranking = user_rankings_service.get_user_ranking(user_id, survey_id)
            rejections = user_rankings_service.get_user_rejections(user_id, survey_id)

        happiness = get_happiness(choice_id, ranking, rejections)
        if isinstance(happiness, (int, float)):
            happiness_sum += happiness
            valid_count += 1
            happiness_results[happiness] = happiness_results.get(happiness, 0) + 1
        else:
            happiness_results[happiness] = happiness_results.get(happiness, 0) + 1

    return happiness_sum, happiness_results, valid_count


def get_happiness(survey_choice_id, user_ranking, user_rejections):
    """
    A function for getting the ordinal number of the survey_choice which the student ended in. E.G rankings = "2,4,5,1,3" and they
    got chosen for 4, the function returns 2.

    args:
        survey_choice_id: The id of the survey choice in which the student was selected into
        user_ranking: The ranking of the user for the survey
    """
    rejections_list = convert_to_int_list(user_rejections)

    if survey_choice_id in rejections_list:
        return gettext("Kielletty")

    ranking_list = convert_to_list(user_ranking)
    happiness = 0
    for choice_id in ranking_list:
        happiness += 1
        if survey_choice_id == int(choice_id):
            return happiness

    return "Ei järjestetty"


def happiness_sort_key(x):
    """
    A sort key function for sorting happiness results so that integers come first
    in ascending order, then "Ei järjestettyyn", then "Kiellettyyn".
    """
    value = x[0]
    if isinstance(value, int):
        return (0, value)
    elif value == "Ei järjestettyyn":
        return (1, 0)
    elif value == gettext("Kiellettyyn"):
        return (2, 0)
    else:
        # Any other string (shouldn't happen)
        return (3, 0)


def dropped_group_names(dropped_groups_id):
    """
    Get the names of dropped groups by their ids

    args:
        dropped_groups_id: A list of ids of dropped groups

    returns:
        A list of names of dropped groups
    """
    dropped_groups = []
    for group_id in dropped_groups_id:
        group = survey_choices_service.get_survey_choice(group_id)
        dropped_groups.append(group["name"])

    return dropped_groups


def absent_students_output(absent_students_dict):
    """
    Build results structure for absent students in a survey.
    Returns a list of absent student dicts.
    """
    output_data = []
    for student_id, student in absent_students_dict.items():
        student_entry = [
            [student.id, student.name],
            user_service.get_email(student.id),
            [None, "Absent"],
        ]
        output_data.append(student_entry)
    return output_data


def update_participation_counts(allocation_result, participation_limit_group_names, participation_counts):
    """
    Update participation counts based on the output data from the hungarian algorithm.

    args:
        output_data: The output data from the hungarian algorithm
        students_dict: A dict containing users which have been converted into students entities.
        participation_limit_group_names: { choice_id: choice_name } for choices with limits
        participation_counts: { user_id: { choice_name: count } } tracking current counts
    """
    for entry in allocation_result:
        student_info = entry[0]
        assigned_group = entry[2]
        if not student_info or not assigned_group:
            continue
        user_id = student_info[0]
        group_id = assigned_group[0]
        if group_id in participation_limit_group_names:
            name = participation_limit_group_names[group_id]
            user_counts = participation_counts.setdefault(user_id, {})
            user_counts[name] = user_counts.get(name, 0) + 1


def get_participation_limits(survey_id, stages):
    """
    Get participation limits and corresponding groups from survey stages.

    args:
        stages: The stages of the survey

    Returns:
      participation_limits: { choice_name: limit } for limits > 0
      participation_limit_groups: { choice_id: choice_name } for those choices
    """

    participation_limits = {}
    participation_limit_groups = {}
    for stage in stages:
        stage_choices = survey_choices_service.get_list_of_stage_survey_choices(survey_id, stage.stage)

        for choice in stage_choices:
            cid = choice["id"]
            name = choice["name"]
            limit = choice.get("participation_limit", 0)
            if limit > 0:
                participation_limits[name] = limit
                participation_limit_groups[cid] = name

    return participation_limits, participation_limit_groups


def prune_students_for_limits(students_dict, participation_limit_groups, participation_limits, participation_counts):
    """
    Prune students' selections to enforce participation limits.

    args:
        students_dict: A dict containing users which have been converted into students entities.
        participation_limit_groups: { choice_id: choice_name } for choices with limits
        participation_limits: { choice_name: limit } for limits > 0
        participation_counts: { user_id: { choice_name: count } } tracking current counts
    """
    for user_id, student in students_dict.items():
        user_counts = participation_counts.setdefault(user_id, {})
        new_selections = []
        for sel in student.selections:
            if sel in participation_limit_groups:
                name = participation_limit_groups[sel]
                limit = participation_limits.get(name, 0)
                if user_counts.get(name, 0) >= limit:
                    # skip this selection — student already reached limit for this name
                    continue
            new_selections.append(sel)
        student.selections = new_selections


def convert_choices_groups(survey_choices):
    """
    Converts database data into the class "Group", which is used in the sorting algorithm

    args:
        survey_choices: The list of choices for a survey
    """
    groups = {}
    for choice in survey_choices:
        cid = choice["id"]
        name = choice["name"]
        max_spaces = choice.get("max_spaces", choice.get("spaces"))
        min_size = choice.get("min_size", choice.get("minSize"))
        participation_limit = choice.get("participation_limit", 0)
        mandatory = choice.get("mandatory", choice.get("hidden", False))

        groups[cid] = Group(cid, name, max_spaces, min_size, participation_limit, mandatory)
    return groups


def convert_users_students(user_rankings, allow_absences=False):
    """
    Converts database data into the class "Student", which is used in the sorting algorithm

    args:
        user_rankings: The list of user rankings for a survey
        allow_absences: Whether to include absent students or not

    Returns:
        If allow_absences is True, returns a tuple of two dicts: (students, absent_students).
        If allow_absences is False, returns only the students dict.
    """
    students = {}
    absent_students = {}
    for user_ranking in user_rankings:
        user_id = user_ranking[0]
        name = user_service.get_name(user_id)
        ranking = convert_to_list(user_ranking[1])
        int_ranking = [int(i) for i in ranking]
        int_rejections = []
        if user_ranking[2]:
            if len(user_ranking[2]) > 0:
                rejections = convert_to_list(user_ranking[2])
                int_rejections = [int(i) for i in rejections]

        if allow_absences:
            if user_ranking[4]:
                absent_students[user_id] = Student(user_id, name, int_ranking, int_rejections, not_available=user_ranking[4])
            else:
                students[user_id] = Student(user_id, name, int_ranking, int_rejections)
        else:
            students[user_id] = Student(user_id, name, int_ranking, int_rejections)

    if allow_absences:
        return students, absent_students
    return students


def convert_date(data):
    """
    Convert a datetime object to a dd.mm.yyyy string

    args:
        data: The datetime object
    """
    day = check_if_zero_needed(str(data.day))
    month = check_if_zero_needed(str(data.month))
    year = str(data.year)
    date = day + "." + month + "." + year
    return date


def convert_time(data):
    """
    Convert a datetime object to a hh:mm string

    args:
        data: The datetime object
    """
    time_hour = check_if_zero_needed(str(data.hour))
    time_minute = check_if_zero_needed(str(data.minute))
    time = time_hour + ":" + time_minute
    return time


def check_if_zero_needed(unit):
    """
    Add a 0 to the start of the unit if it's length is 1.

    args:
        unit: hour/minute/day/month of a datetime object
    """
    if len(unit) == 1:
        unit = "0" + unit
    return unit
