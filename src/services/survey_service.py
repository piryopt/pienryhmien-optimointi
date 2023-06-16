from flask import session
from repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class SurveyService:
    def __init__(self, survey_repositroy=default_survey_repository):
        self._survey_repository = survey_repositroy

    def get_list_of_survey_choices(self, survey_id):
        if self._survey_repository.check_if_survey_exists(survey_id):
            survey_choices = self._survey_repository.find_survey_choices(survey_id)
            return survey_choices
        return False
    
    def new_user_ranking(self, survey_id, ranking):
        user_id = session.get("user_id", 0)
        if user_id == 0:
            print("MUST BE LOGGED IN!")
            return False
        if not self.user_ranking_exists(user_id, survey_id):
            if self._survey_repository.new_user_ranking(user_id, survey_id, ranking):
                return True
        print("ERROR IN ADDING NEW USER RANKING!")
        return False
    
    def user_ranking_exists(self, user_id, survey_id):
        if not self._survey_repository.check_if_ranking_exists(user_id, survey_id):
            return False
        print("USER RANKING ALREADY EXISTS!")
        return True


survey_service = SurveyService()