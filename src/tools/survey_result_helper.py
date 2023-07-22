from src.entities.group import Group
from src.entities.student import Student
from src.services.user_service import user_service
from src.tools.rankings_converter import convert_to_list

def convert_choices_groups(survey_choices):
    groups = {}
    for choice in survey_choices:
        groups[choice[0]] = Group(choice[0], choice[2], choice[3])
    return groups

def convert_users_students(user_rankings):
    students = {}
    for user_ranking in user_rankings:
        user_id = user_ranking[0]
        name = user_service.get_name(user_id)
        ranking = convert_to_list(user_ranking[1])
        int_ranking = [int(i) for i in ranking]
        students[user_id] = Student(user_id, name, int_ranking)
    return students

def get_happiness(survey_choice_id, user_ranking):
    ranking_list = convert_to_list(user_ranking)
    happiness = 0
    for choice_id in ranking_list:
        happiness += 1
        if survey_choice_id == int(choice_id):
            break
    return happiness
    