from src.repositories.survey_choices_repository import (
    survey_choices_repository as default_survey_choices_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class SurveyChoicesService:
    def __init__(self, survey_choices_repository = default_survey_choices_repository, survey_repository = default_survey_repository):
        self._survey_choices_repository = survey_choices_repository
        self._survey_repository = survey_repository

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

    def get_choice_name_and_spaces(self, choice_id):

        # take only the needed columns
        data = self._survey_choices_repository.get_survey_choice(choice_id)
        return (data[2], data[3])

    def get_choice_additional_infos(self, choice_id):
        return self._survey_choices_repository.get_choice_additional_infos(choice_id)

survey_choices_service = SurveyChoicesService()
