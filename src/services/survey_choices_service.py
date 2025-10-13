from src.repositories.survey_choices_repository import survey_choices_repository as default_survey_choices_repository
from src.repositories.survey_repository import survey_repository as default_survey_repository


class SurveyChoicesService:
    def __init__(self, survey_choices_repository=default_survey_choices_repository, survey_repository=default_survey_repository):
        """
        Initalized the service for survey choices with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            survey_choices_repository: The repository for survey choices
            survey_repository: The repository for surveys

        """
        self._survey_choices_repository = survey_choices_repository
        self._survey_repository = survey_repository

    def get_list_of_survey_choices(self, survey_id: str):
        """
        Returns a list of survey choices from a survey

        args:
            survey_id: The id of the survey from which we want the survey choices
        """
        return self._survey_choices_repository.find_survey_choices(survey_id)

    def get_survey_choice(self, survey_choice_id: int):
        """
        Returns the data of a survey choice

        args:
            survey_choice_id: The id of the survey choice
        """
        return self._survey_choices_repository.get_survey_choice(survey_choice_id)

    def get_survey_choice_min_size(self, survey_choice_id: int):
        """
        Returns the min_size of a survey choice

        args:
            survey_choice_id: The id of the survey choice
        """
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            return None
        return survey_choice.min_size

    def get_choice_name_and_spaces(self, choice_id: int):
        """
        Get the name and spaces from a survey choice

        args:
            choice_id: The id of the survey choice
        """
        # take only the needed columns
        data = self._survey_choices_repository.get_survey_choice(choice_id)
        if not data:
            return None
        return (data.id, data.name, data.max_spaces)

    def get_choice_additional_infos(self, choice_id: int):
        """
        Get all info of a survey choice except name and spaces

        args:
            choice_id: The id of the survey choice
        """
        return self._survey_choices_repository.get_choice_additional_infos(choice_id)

    def get_choice_additional_infos_not_hidden(self, choice_id: int):
        """
        Get all info of a survey choice except name and spaces

        args:
            choice_id: The id of the survey choice
        """
        return self._survey_choices_repository.get_choice_additional_infos_not_hidden(choice_id)

    def survey_all_additional_infos(self, survey_id):
        """
        Get additional info on all choices of a given survey.

        args:
            survey_id: The id of the survey
        """
        return self._survey_choices_repository.get_all_additional_infos(survey_id)

    def count_number_of_available_spaces(self, survey_id: str):
        """
        Returns int of the total number of available space in the groups of a survey

        Args:
            survey_id (str): id for the survey
        """
        choices = self.get_list_of_survey_choices(survey_id)

        tally = sum(choice.max_spaces for choice in choices)

        return tally

    def add_empty_survey_choice(self, survey_id: str, spaces: int):
        """
        If a survey has more answers than availeble spaces, the teacher can choose
        to add a non-choice where students who can't fit in their choice will be put
        Args:
            survey_id (str): ID of the survey
            spaces (int): Number of spaces needed in the group, equal to extra answers
            in the survey
        """
        return self._survey_choices_repository.create_new_survey_choice(survey_id, "Tyhjä", spaces, 0, False)

    def check_answers_less_than_min_size(self, survey_id, survey_answers_amount):
        """
        Check if there are less answers than the group with the smallest min_size

        Args:
            survey_id: id for the survey
            survey_answers_amount: The amount of answers for a survey
        """
        choices = self.get_list_of_survey_choices(survey_id)
        if not choices:
            return False
        for choice in choices:
            if survey_answers_amount > choice.min_size:
                return False
        return True

    def get_survey_choice_mandatory(self, survey_choice_id: int):
        """
        Returns a boolean indicating if the survey choice is mandatory

        args:
            survey_choice_id: The id of the survey choice
        """
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            return None
        return survey_choice.mandatory


survey_choices_service = SurveyChoicesService()
