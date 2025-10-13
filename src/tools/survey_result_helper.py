from src.entities.group import Group
from src.entities.student import Student
from src.services.user_service import user_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.tools.rankings_converter import convert_to_list, convert_to_int_list
from flask_babel import gettext
import src.algorithms.hungarian as h
import src.algorithms.weights as w
import copy


def hungarian_results(survey_id, user_rankings, groups_dict, students_dict, survey_choices):
    """
    Run the hungarian algorthim until their is no violation for the min_size portion

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

    output_data, unranked_or_rejected = run_hungarian(survey_id, survey_answers_amount, groups_dict, students_dict, dropped_groups_id)
    additional_infos, cinfos = get_additional_infos(survey_choices)

    happiness_avg, happiness_results = get_happiness_data(output_data, survey_id)
    happiness_avg /= len(students_dict) - unranked_or_rejected if (len(students_dict) - unranked_or_rejected) > 0 else 1

    happiness_results_list = []
    for k, v in happiness_results.items():
        if v > 0:
            if k == gettext("Hylätty"):
                k = gettext("Hylättyyn")
                msg = gettext(" valintaan sijoitetut käyttäjät: ")
            elif k == gettext("Ei järjestetty"):
                k = gettext("Ei järjestettyyn")
                msg = gettext(" valintaan sijoitetut käyttäjät: ")
            else:
                msg = gettext(". valintaansa sijoitetut käyttäjät: ")
            happiness_results_list.append((k, msg + f"{v}"))

    happiness_results_list.sort(key=happiness_sort_key)
    dropped_groups = dropped_group_names(dropped_groups_id)

    output_data = (output_data, happiness_avg, happiness_results_list, dropped_groups, cinfos, additional_infos)
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
            groups_dict[empty_group[0]] = Group(empty_group[0], empty_group[2], empty_group[3], empty_group[5], empty_group[6])

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
            min_size = survey_choices_service.get_survey_choice_min_size(survey_choice_id)
            mandatory = survey_choices_service.get_survey_choice_mandatory(survey_choice_id)

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
            return output_data, unranked_or_rejected


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

        # Skip students in other mandatory groups if they prefer their current mandatory group more
        if survey_choices_service.get_survey_choice_mandatory(assigned_group):
            current_group_rank = rank(students_dict, student_id, assigned_group)
            target_group_rank = rank(students_dict, student_id, survey_choice_id)
            current_group_min_size = survey_choices_service.get_survey_choice_min_size(assigned_group)

            if current_group_rank <= target_group_rank and group_sizes[assigned_group] <= current_group_min_size:
                students_in_mandatory_groups.append((i, student_id, assigned_group))
                continue

        candidates.append((i, student_id, assigned_group))

    # If not enough candidates, Phase 2: pull from any group (respect min_size for mandatory groups)
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
        additional_infos[str(row[0])] = []

        cinfos = survey_choices_service.get_choice_additional_infos(row[0])
        for i in cinfos:
            additional_infos[str(row[0])].append(i[1])

    return additional_infos, cinfos


def get_happiness_data(output_data, survey_id):
    """
    Extract happiness data from the output data.

    args:
        output_data: The output data from the hungarian algorithm along with happiness average, happiness results, dropped groups and additional infos
    """
    happiness_results = {}
    happiness_avg = 0
    for results in output_data:
        user_id = results[0][0]
        choice_id = results[2][0]
        ranking = user_rankings_service.get_user_ranking(user_id, survey_id)
        rejections = user_rankings_service.get_user_rejections(user_id, survey_id)
        happiness = get_happiness(choice_id, ranking, rejections)
        if happiness != gettext("Hylätty") and happiness != gettext("Ei järjestetty"):
            happiness_avg += happiness
        results.append(happiness)
        if happiness not in happiness_results:
            happiness_results[happiness] = 1
        else:
            happiness_results[happiness] += 1

    return happiness_avg, happiness_results


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
        return gettext("Hylätty")

    ranking_list = convert_to_list(user_ranking)
    happiness = 0
    for choice_id in ranking_list:
        happiness += 1
        if survey_choice_id == int(choice_id):
            return happiness

    return gettext("Ei järjestetty")


def happiness_sort_key(x):
    """
    A sort key function for sorting happiness results so that integers come first
    in ascending order, then "Ei järjestettyyn", then "Hylättyyn".
    """
    value = x[0]
    if isinstance(value, int):
        return (0, value)
    elif value == gettext("Ei järjestettyyn"):
        return (1, 0)
    elif value == gettext("Hylättyyn"):
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
        dropped_groups.append(group.name)

    return dropped_groups


def convert_choices_groups(survey_choices):
    """
    Converts database data into the class "Group", which is used in the sorting algorithm

    args:
        survey_choices: The list of choices for a survey
    """
    groups = {}
    for choice in survey_choices:
        groups[choice[0]] = Group(choice[0], choice[2], choice[3], choice[5], choice[6])
    return groups


def convert_users_students(user_rankings):
    """
    Converts database data into the class "Student", which is used in the sorting algorithm

    args:
        user_rankings: The list of user rankings for a survey
    """
    students = {}
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
        students[user_id] = Student(user_id, name, int_ranking, int_rejections)
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
