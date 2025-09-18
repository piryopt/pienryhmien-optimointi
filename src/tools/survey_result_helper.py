from src.entities.group import Group
from src.entities.student import Student
from src.services.user_service import user_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.tools.rankings_converter import convert_to_list
from datetime import datetime
from flask_babel import gettext
import src.algorithms.hungarian as h
import src.algorithms.weights as w

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
            if len(user_ranking[2])>0:
                rejections = convert_to_list(user_ranking[2])
                int_rejections = [int(i) for i in rejections]
        students[user_id] = Student(user_id, name, int_ranking, int_rejections)
    return students

def get_happiness(survey_choice_id, user_ranking):
    """
    A function for getting the ordinal number of the survey_choice which the student ended in. E.G rankings = "2,4,5,1,3" and they
    got chosen for 4, the function returns 2.

    args:
        survey_choice_id: The id of the survey choice in which the student was selected into
        user_ranking: The ranking of the user for the survey
    """
    ranking_list = convert_to_list(user_ranking)
    happiness = 0
    for choice_id in ranking_list:
        happiness += 1
        if survey_choice_id == int(choice_id):
            break
    return happiness
    
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
        unit = "0"+ unit
    return unit

def hungarian_results(survey_id, user_rankings, groups_dict, students_dict, survey_choices):
    """
    Run the hungarian algorthim until their is no violation for the min_size portion

    args:
        survey_id: The id of the survey
        user_rankings: The rankings for the survey in question
        groups_dict: A dict containing survey choices which have been converted into group entities. Needed for the hungarian algorithm
        students_dict: A dict containing users which have been converted into students entities. Needed for the hungarian algorithm
        survey_choices: The choices of the survey in question
    """
    survey_answers_amount = len(user_rankings)
    dropped_groups_id = []

    output_data = run_hungarian(survey_id, survey_answers_amount, groups_dict, students_dict, dropped_groups_id)

    # Create a dict which contains choice's additional info as list
    additional_infos = {}
    for row in survey_choices:
        additional_infos[str(row[0])] = []
        
        cinfos = survey_choices_service.get_choice_additional_infos(row[0])
        for i in cinfos:
            additional_infos[str(row[0])].append(i[1])

    # Add to data the number of the choice that the user got. Also update happiness data displayed.
    happiness_avg = 0
    happiness_results = {}
    for results in output_data:
        user_id = results[0][0]
        choice_id =  results[2][0]
        ranking = user_rankings_service.get_user_ranking(user_id, survey_id)
        happiness = get_happiness(choice_id, ranking)
        happiness_avg += happiness
        results.append(happiness)
        if happiness not in happiness_results:
            happiness_results[happiness] = 1
        else:
            happiness_results[happiness] += 1
    happiness_avg /= len(students_dict)
    happiness_results_list = []
    for k,v in happiness_results.items():
        if v > 0:
            msg = gettext('. valintaansa sijoitetut käyttäjät: ')
            happiness_results_list.append((k, msg + f"{v}"))
    
    # Fix a bug where happiness results did not always come in the right order
    happiness_results_list.sort()
    
    dropped_groups = []
    for group_id in dropped_groups_id:
        group = survey_choices_service.get_survey_choice(group_id)
        dropped_groups.append(group.name)

    output_data = (output_data, happiness_avg, happiness_results_list, dropped_groups, additional_infos, cinfos)
    return output_data

def run_hungarian(survey_id, survey_answers_amount, groups_dict, students_dict, dropped_groups_id):
    """
    Run the hungarian algorithm until no violation.
    """
    loop = True
    while loop:
        seats = get_seats(groups_dict)

        # If there are less seats than survey answers, add an empty group 
        if seats < survey_answers_amount:
            empty_group_id = survey_choices_service.add_empty_survey_choice(survey_id, survey_answers_amount-seats)
            empty_group = survey_choices_service.get_survey_choice(empty_group_id)
            groups_dict[empty_group[0]] = Group(empty_group[0], empty_group[2], empty_group[3], empty_group[5], empty_group[6])

        # Run the algotrithm with the groups that haven't been dropped
        weights = w.Weights(len(groups_dict), len(students_dict)).get_weights()
        sort = h.Hungarian(groups_dict, students_dict, weights)
        sort.run()
        output_data = sort.get_data()

        # Count how many students each group has
        group_sizes = {}
        for id, group in groups_dict.items():
            group_sizes[id] = 0
        for [student_data, student_email, group_data] in output_data:
            group_id = group_data[0]
            group_sizes[group_id] += 1

        # Check if min_size is greater than group size. If it is, remove the group_id that has the worst ranking from all relevant lists and dictionaries.
        violation = False
        sorted_groups = [k for k, v in sorted(group_sizes.items(), key=lambda item: item[1])]

        for survey_choice_id in sorted_groups:
            min_size = survey_choices_service.get_survey_choice_min_size(survey_choice_id)
            mandatory = survey_choices_service.get_survey_choice_mandatory(survey_choice_id)
            if min_size > group_sizes[survey_choice_id]:
                if mandatory:
                    # If the group is mandatory, we can't drop it
                    mandatory_group_violation = True
                    continue
                violation = True
                mandatory_group_violation = False
                # Remove dropped group from groups_dict and student selections so that it doesn't affect the next round
                groups_dict.pop(survey_choice_id)
                dropped_groups_id.append(survey_choice_id)
                for user_id, student in students_dict.items():
                    if survey_choice_id in student.selections:
                        student.selections.remove(survey_choice_id)
                    if survey_choice_id in student.rejections:
                        student.rejections.remove(survey_choice_id)
                break

        if mandatory_group_violation and not violation:
            # There was a mandatory group violation but no other violations, 
            # so we have to drop a group even if it meets the min_size requirement
            violation = True
            mandatory_group_violation = False
            
            for survey_choice_id in sorted_groups:
                mandatory = survey_choices_service.get_survey_choice_mandatory(survey_choice_id)
                if not mandatory:
                    groups_dict.pop(survey_choice_id)
                    dropped_groups_id.append(survey_choice_id)
                    for user_id, student in students_dict.items():
                        if survey_choice_id in student.selections:
                            student.selections.remove(survey_choice_id)
                        if survey_choice_id in student.rejections:
                            student.rejections.remove(survey_choice_id)
                break

        if not violation:
            return output_data


def get_seats(groups_dict):
    """
    Get the amount of available seats in the remaining groups
    """
    seats = 0
    for id, group in groups_dict.items():
        seats += group.size
    return seats
