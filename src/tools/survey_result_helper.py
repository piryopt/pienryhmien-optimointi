from src.entities.group import Group
from src.entities.student import Student
from src.services.user_service import user_service
from src.tools.rankings_converter import convert_to_list
from datetime import datetime

def convert_choices_groups(survey_choices):
    """
    Converts database data into the class "Group", which is used in the sorting algorithm

    args:
        survey_choices: The list of choices for a survey
    """
    groups = {}
    for choice in survey_choices:
        groups[choice[0]] = Group(choice[0], choice[2], choice[3])
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
        rejections = convert_to_list(user_ranking[2])
        int_rejections = []
        if len(int_rejections) > 0:
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
