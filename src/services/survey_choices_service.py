from src.repositories.survey_choices_repository import (
    survey_choices_repository as default_survey_choices_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class SurveyChoicesService:
    def __init__(self, survey_choices_repository = default_survey_choices_repository, survey_repository = default_survey_repository):
        """
        Initalized the service for survey choices with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            survey_choices_repository: The repository for survey choices
            survey_repository: The repository for surveys

        """
        self._survey_choices_repository = survey_choices_repository
        self._survey_repository = survey_repository

    def get_list_of_survey_choices(self, survey_id):
        """
        Returns a list of survey choices from a survey

        args:
            survey_id: The id of the survey from which we want the survey choices
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        survey_choices = self._survey_choices_repository.find_survey_choices(survey_id)
        return survey_choices

    def get_survey_choice(self, survey_choice_id):
        """
        Returns the data of a survey choice

        args:
            survey_choice_id: The id of the survey choice
        """
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            return False
        return survey_choice

    def get_choice_name_and_spaces(self, choice_id):
        """
        Get the name and spaces from a survey choice

        args:
            choice_id: The id of the survey choice
        """
        # take only the needed columns
        data = self._survey_choices_repository.get_survey_choice(choice_id)
        return (data[0],data[2], data[3])

    def get_choice_additional_infos(self, choice_id):
        """
        Get all info of a survey choice except name and spaces

        args:
            choice_id: The id of the survey choice
        """
        return self._survey_choices_repository.get_choice_additional_infos(choice_id)

survey_choices_service = SurveyChoicesService()
