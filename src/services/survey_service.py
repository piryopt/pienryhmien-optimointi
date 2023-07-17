from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)
from src.tools.parsers import parser_elomake_csv, parser_manual

class SurveyService:
    def __init__(self, survey_repositroy=default_survey_repository):
        self._survey_repository = survey_repositroy

    def get_survey_name(self, survey_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        return survey[1]

    def add_new_survey(self, surveyname, teacher_id):
        if self._survey_repository.survey_name_exists(surveyname, teacher_id):
            print("A SURVEY WITH THIS NAME ALREADY EXISTS!")
            return False
        if len(surveyname) < 4:
            print("The name is too short!")
            return False
        survey_id = self._survey_repository.add_new_survey(surveyname, teacher_id)
        if not survey_id:
            return False
        return survey_id

    def count_surveys_created(self, user_id):
        list_n = self._survey_repository.count_created_surveys(user_id)
        if not list_n:
            return 0
        return list_n

    def close_survey(self, survey_id, teacher_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        if survey.teacher_id != teacher_id:
            print("YOU DID NOT CREATE THIS SURVEY. YOU CANNOT CLOSE IT")
            return False
        return self._survey_repository.close_survey(survey_id, teacher_id)
    
    def open_survey(self, survey_id, teacher_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        if survey.teacher_id != teacher_id:
            print("YOU DID NOT CREATE THIS SURVEY. YOU CANNOT OPEN IT")
            return False
        if self._survey_repository.survey_name_exists(survey.surveyname, teacher_id):
            print("A SURVEY WITH THIS NAME ALREADY EXISTS!")
            return False
        return self._survey_repository.open_survey(survey_id, teacher_id)

    def get_active_surveys(self, teacher_id):
        surveys = self._survey_repository.get_active_surveys(teacher_id)
        if not surveys:
            print("THIS USER HAS NOT CREATED ANY SURVEYS!")
            return False
        return surveys
    
    def check_if_survey_closed(self, survey_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        closed = survey.closed
        return closed
    
    def get_list_closed_surveys(self, teacher_id):
        surveys = self._survey_repository.get_closed_surveys(teacher_id)
        return surveys

    def update_survey_answered(self, survey_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        saved = self._survey_repository.update_survey_answered(survey_id)
        return saved

    def check_if_survey_results_saved(self, survey_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        return survey.results_saved

    
    def create_survey_from_csv(self, file, survey_name, user_id):
        parser_elomake_csv(file, survey_name, user_id) # in tools

    def get_choice_additional_infos(self, choice_id):
        return self._survey_repository.get_choice_additional_infos(choice_id)

    def get_choice_name_and_spaces(self, choice_id):
        return self._survey_repository.get_choice_name_and_spaces(choice_id)
    
    def create_new_survey_manual(self, survey_choices,survey_name, user_id):
        parser_manual(survey_choices, survey_name, user_id)

survey_service = SurveyService()
