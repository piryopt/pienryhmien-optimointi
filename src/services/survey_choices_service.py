from src.repositories.survey_choices_repository import (
    survey_choices_repository as default_survey_choices_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)
from src.repositories.choice_infos_repository import (
    choice_infos_repository as default_choice_infos_repository
)

class SurveyChoicesService:
    def __init__(self, survey_choices_repository = default_survey_choices_repository,
                  survey_repository = default_survey_repository, choice_infos_repository = default_choice_infos_repository):
        self._survey_choices_repository = survey_choices_repository
        self._survey_repository = survey_repository
        self._choice_infos_repository = choice_infos_repository

    def get_list_of_survey_choices(self, survey_id):
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        survey_choices = self._survey_choices_repository.find_survey_choices(survey_id)
        return survey_choices
    
    def get_survey_choice(self, survey_choice_id):
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            print("SURVEY CHOICE NOT FOUND!")
            return False
        return survey_choice
    
    def add_survey_choice(self, survey_id, name, max_spaces, info1, info2):
        survey_exists = self._survey_repository.get_survey(survey_id)
        if not survey_exists:
            print("SURVEY DOES NOT EXIST!")
            return False
        if len(name) < 3:
            print("The name is too short!")
            return False
        new_choice = self._survey_choices_repository.add_new_survey_choice(survey_id, name, max_spaces, info1, info2)
        if not new_choice:
            return False
        return True
    
    def get_choice_name_and_spaces(self, choice_id):
        return self._choice_infos_repository.get_choice_name_and_spaces(choice_id)
    
    def get_choice_additional_infos(self, choice_id):
            return self._choice_infos_repository.get_choice_additional_infos(choice_id)

survey_choices_service = SurveyChoicesService()
