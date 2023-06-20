from flask import session
from repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class SurveyService:
    def __init__(self, survey_repositroy=default_survey_repository):
        self._survey_repository = survey_repositroy

    def get_list_of_survey_choices(self, survey_id):
        survey = self._survey_repository.check_if_survey_exists(survey_id)
        if not survey:
            return False
        survey_choices = self._survey_repository.find_survey_choices(survey_id)
        return survey_choices

    def get_survey_name(self, survey_id):
        survey = self._survey_repository.check_if_survey_exists(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        return survey[1]

    def new_user_ranking(self, survey_id, ranking):
        user_id = session.get("user_id", 0)
        if user_id == 0:
            print("MUST BE LOGGED IN!")
            return False
        if not self.user_ranking_exists(survey_id):
            if self._survey_repository.new_user_ranking(user_id, survey_id, ranking):
                return True
        print("ERROR IN ADDING NEW USER RANKING!")
        return False

    def user_ranking_exists(self, survey_id):
        user_id = session.get("user_id", 0)
        ranking = self._survey_repository.get_user_ranking(user_id, survey_id)
        if not ranking:
            return False
        return ranking

    def delete_ranking(self, survey_id):
        current_user_id = session.get("user_id", 0)
        ranking = self._survey_repository.get_user_ranking(current_user_id, survey_id)
        if not ranking:
            print("NO RANKING FOR THIS SURVEY!")
            return False
        if self._survey_repository.delete_user_ranking(current_user_id, survey_id):
            return True
        print("ERROR IN DELETING RANKING")
        return False

    def get_survey_choice(self, survey_choice_id):
        survey_choice = self._survey_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            print("SURVEY CHOICE NOT FOUND!")
            return False
        return survey_choice

    def add_user_ranking(self, survey_id, ranking):
        user_id = session.get("user_id",0)
        self._survey_repository.add_user_ranking(user_id,survey_id,ranking)
        return True
    
    def add_new_survey(self, surveyname):
        if self._survey_repository.survey_name_exists(surveyname):
            print("A SURVEY WITH THIS NAME ALREADY EXISTS!")
            return False
        if len(surveyname) < 4:
            print("The name is too short!")
            return False
        survey_id = self._survey_repository.add_new_survey(surveyname)
        if not survey_id:
            return False
        return survey_id
    
    def add_survey_choice(self, survey_id, name, max_spaces, info1, info2):
        survey_exists = self._survey_repository.check_if_survey_exists(survey_id)
        if not survey_exists:
            print("SURVEY DOES NOT EXIST!")
            return False
        if len(name) < 3:
            print("The name is too short!")
            return False
        new_choice = self._survey_repository.add_new_survey_choice(survey_id, name, max_spaces, info1, info2)
        if not new_choice:
            return False
        return True


        

survey_service = SurveyService()
