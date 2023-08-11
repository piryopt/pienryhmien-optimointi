from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)
from src.repositories.survey_teachers_repository import (
    survey_teachers_repository as default_survey_teachers_repository
)
from src.tools.parsers import parser_elomake_csv_to_dict, parser_dict_to_survey, parser_existing_survey_to_dict

class SurveyService:
    def __init__(self, survey_repositroy=default_survey_repository, survey_teachers_repository = default_survey_teachers_repository):
        """
        Initalizes the service for surveys with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository
        
        args and variables:
            survey_repository: The repository for surveys

        """
        self._survey_repository = survey_repositroy
        self._survey_teachers_repository = survey_teachers_repository

    def get_survey_name(self, survey_id):
        """
        Get the name of the survey

        args:
            survey_id: The id of the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        return survey[1]

    def count_surveys_created(self, user_id):
        """
        Get the size of the list of surveys created. If no surveys have been created, return 0

        args:
            user_id: The id of the user whose list of surveys we want
        """
        list_n = self._survey_repository.count_created_surveys(user_id)
        if not list_n:
            return 0
        return list_n

    def close_survey(self, survey_id, teacher_id):
        """
        Close the survey, so that no more rankings can be added

        args:
            survey_id: The id of the survey
            teacher_id: The id of the user, who is attempting to close the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        # Only the teacher who created the survey can close it
        teacher_exists = self._survey_teachers_repository.check_if_teacher_in_survey(survey_id, teacher_id)
        if not teacher_exists:
            return False
        return self._survey_repository.close_survey(survey_id)

    def open_survey(self, survey_id, teacher_id):
        """
        Re-open the survey, so that rankings can be added

        args:
            survey_id: The id of the survey
            teacher_id: The id of the user, who is attempting to open the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        # Only the teacher who created the survey can open it
        teacher_exists = self._survey_teachers_repository.check_if_teacher_in_survey(survey_id, teacher_id)
        if not teacher_exists:
            return False
        if self._survey_repository.survey_name_exists(survey.surveyname, teacher_id):
            return False
        return self._survey_repository.open_survey(survey_id)

    def get_active_surveys(self, teacher_id):
        """
        Get the list of active surveys for a user

        args:
            teacher_id: The id of the user whose active surveys we want
        """
        surveys = self._survey_repository.get_active_surveys(teacher_id)
        if not surveys:
            return False
        return surveys

    def check_if_survey_closed(self, survey_id):
        """
        Check if the survey is open or closed

        args:
            survey_id: The id of the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        closed = survey.closed
        return closed

    def get_list_closed_surveys(self, teacher_id):
        """
        Get the list of closed surveys for a user

        args:
            teacher_id: The id of the user whose closed surveys we want
        """
        surveys = self._survey_repository.get_closed_surveys(teacher_id)
        return surveys

    def update_survey_answered(self, survey_id):
        """
        Updates the survey of which the results have been saved into the database, so that they cannot be saved again

        args:
            survey_id: The id of the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        saved = self._survey_repository.update_survey_answered(survey_id)
        return saved

    def check_if_survey_results_saved(self, survey_id):
        """
        Checks the survey if the results have been saved into the database

        args:
            survey_id: The id of the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        return survey.results_saved

    def create_survey_from_csv(self, file):
        '''
        Calls tools.parsers Elomake csv to dict parser
        RETURNS the dictionary
        '''
        return parser_elomake_csv_to_dict(file) # in tools
    
    def create_new_survey_manual(self, survey_choices, survey_name, user_id, description, minchoices, date_begin, time_begin, date_end, time_end):
        '''
        Calls tools.parsers dictionary to survey parser
        that creates the survey, its choices and their additional infos
        RETURNS created survey's id
        '''
        if self._survey_repository.survey_name_exists(survey_name, user_id):
            return False

        return parser_dict_to_survey(survey_choices, survey_name, description, minchoices, date_begin, time_begin, date_end, time_end)

    def get_survey_description(self, survey_id):
        """
        Gets the description of the survey

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.get_survey_description(survey_id)
    
    def get_survey_enddate(self, survey_id):
        """
        Gets the enddate of the survey

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.get_survey_time_end(survey_id)

    def get_survey_min_choices(self, survey_id):
        """
        Returns the amount of minumum answers required in the survey.

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.get_survey_min_choices(survey_id)

    def get_survey_as_dict(self, survey_id):
        '''
        Gets survey, its choices and their additional infos as dictionary
        RETURNS dictionary
        '''
        return parser_existing_survey_to_dict(survey_id)
    
    def get_list_active_answered(self, user_id):
        """
        Gets a list of active surveys that the user has answered.

        args:
            user_id: The id of the user
        """
        active = self._survey_repository.get_list_active_answered(user_id)
        if not active:
            return []
        return active
    
    def get_list_closed_answered(self, user_id):
        """
        Gets a list of closed surveys that the user has answered.

        args:
            user_id: The id of the user
        """
        closed = self._survey_repository.get_list_closed_answered(user_id)
        if not closed:
            return []
        return closed
    
    def fetch_survey_responses(self, survey_id):
        """
        Gets a list of user_survey_rankings for the survey
        
        args:
            survey_id: The id of the survey
        """
        rankings = self._survey_repository.fetch_survey_responses(survey_id)
        if not rankings:
            return []
        return rankings

survey_service = SurveyService()
