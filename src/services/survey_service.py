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
        print("USER RANKING ALREADY EXISTS!")
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

survey_service = SurveyService()
