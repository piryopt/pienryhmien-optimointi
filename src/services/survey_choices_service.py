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

    def get_list_of_survey_choices(self, survey_id:str):
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

    def get_survey_choice(self, survey_choice_id:int):
        """
        Returns the data of a survey choice

        args:
            survey_choice_id: The id of the survey choice
        """
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            return False
        return survey_choice
    
    def get_survey_choice_min_size(self, survey_choice_id:int):
        """
        Returns the min_size of a survey choice

        args:
            survey_choice_id: The id of the survey choice
        """
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        if not survey_choice:
            return False
        return survey_choice.min_size

    def get_choice_name_and_spaces(self, choice_id:int):
        """
        Get the name and spaces from a survey choice

        args:
            choice_id: The id of the survey choice
        """
        # take only the needed columns
        data = self._survey_choices_repository.get_survey_choice(choice_id)
        return (data[0],data[2], data[3])

    def get_choice_additional_infos(self, choice_id:int):
        """
        Get all info of a survey choice except name and spaces

        args:
            choice_id: The id of the survey choice
        """
        return self._survey_choices_repository.get_choice_additional_infos(choice_id)
    
    def get_choice_additional_infos_not_hidden(self, choice_id:int):
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
        tally = 0
        for (id, survey_id, name, spaces, deleted, min_size) in choices:
            tally += spaces
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
        return self._survey_choices_repository.create_new_survey_choice(survey_id, "Tyhjä", spaces, 0)
    
    def check_min_equals_max(self, survey_id):
        """
        Check if all survey choices have the same min and max values. Needed for fixing a bug
        where the app crashes in certain cases.

        Args:
            survey_id: id for the survey
        """
        choices = self.get_list_of_survey_choices(survey_id)
        if not choices:
            return (False, 0)
        minmax = choices[0].max_spaces
        for c in choices:
            if c.max_spaces != minmax or c.min_size != minmax:
                return (False, 0)
        return (True, minmax)
    
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



survey_choices_service = SurveyChoicesService()
