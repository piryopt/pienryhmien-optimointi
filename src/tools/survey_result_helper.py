from src.entities.group import Group
from src.entities.student import Student
from src.repositories.user_repository import user_repository

def convert_choices_groups(survey_choices):
    groups = {}
    for choice in survey_choices:
        groups[choice[0]] = Group(choice[0], choice[2], choice[3])
    return groups

def convert_users_students(user_rankings):
    students = {}
    for user_ranking in user_rankings:
        user_id = user_ranking[0]
        user = user_repository.get_user_data(user_id)
        ranking = user_ranking[1].split(",")
        int_ranking = [int(i) for i in ranking]
        student_name = user[0].name
        students[user_id] = Student(user_id, student_name, int_ranking)
    return students
