from datetime import datetime
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)
from src.repositories.survey_owners_repository import (
    survey_owners_repository as default_survey_owners_repository
)
from src.repositories.survey_choices_repository import (
    survey_choices_repository as default_survey_choices_repository
)
from src.tools.parsers import parser_elomake_csv_to_dict, parser_dict_to_survey, parser_existing_survey_to_dict
from src.tools.date_converter import time_to_close
from datetime import datetime
from src.tools.parsers import date_to_sql_valid

class SurveyService:
    def __init__(self, survey_repositroy=default_survey_repository, survey_owners_repository = default_survey_owners_repository, choices_repository = default_survey_choices_repository):
        """
        Initalizes the service for surveys with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository
        
        args and variables:
            survey_repository: The repository for surveys
            survey_owners_repository: The repository for survey owners
            choices_repository: The repository for survey choices


        """
        self._survey_repository = survey_repositroy
        self._survey_owners_repository = survey_owners_repository
        self._choices_repository = choices_repository

    def get_survey(self, survey_id):
        """
        Get all data of a survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        return survey

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

    def close_survey(self, survey_id, user_id):
        """
        Close the survey, so that no more rankings can be added

        args:
            survey_id: The id of the survey
            teacher_id: The id of the user, who is attempting to close the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        # Only a survey owner can close it
        owner_exists = self._survey_owners_repository.check_if_owner_in_survey(survey_id, user_id)
        if not owner_exists:
            return False
        return self._survey_repository.close_survey(survey_id)

    def open_survey(self, survey_id, user_id):
        """
        Re-open the survey, so that rankings can be added

        args:
            survey_id: The id of the survey
            user_id: The id of the user, who is attempting to open the survey
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            return False
        # Only a survey owner can open it
        owner_exists = self._survey_owners_repository.check_if_owner_in_survey(survey_id, user_id)
        if not owner_exists:
            return False
        if self._survey_repository.survey_name_exists(survey.surveyname, user_id):
            return False
        return self._survey_repository.open_survey(survey_id)

    def get_active_surveys(self, user_id):
        """
        Get the list of active surveys for a user

        args:
            user_id: The id of the user whose active surveys we want
        """
        surveys = self._survey_repository.get_active_surveys(user_id)
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

    def get_list_closed_surveys(self, user_id):
        """
        Get the list of closed surveys for a user

        args:
            user_id: The id of the user whose closed surveys we want
        """
        surveys = self._survey_repository.get_closed_surveys(user_id)
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
    
    def create_new_survey_manual(self, survey_choices, survey_name, user_id, description, minchoices, date_end, time_end, allowed_denied_choices=0, allow_search_visibility=True):
        '''
        Calls tools.parsers dictionary to survey parser
        that creates the survey, its choices and their additional infos
        RETURNS created survey's id
        '''
        if self._survey_repository.survey_name_exists(survey_name, user_id):
            return False

        return parser_dict_to_survey(survey_choices, survey_name, description, minchoices, date_end, time_end, allowed_denied_choices, allow_search_visibility)


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

    def get_survey_max_denied_choices(self, survey_id):
        """
        Returns the amount of denied choices the survey allows.

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.get_survey_max_denied_choices(survey_id)
    
    def get_survey_search_visibility(self, survey_id):
        """
        Returns the set preference of showing a choice filtering search bar in the response view of the form.

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.get_survey_search_visibility(survey_id)

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
    
    def check_for_surveys_to_close(self):
        """
        Gets a list of all active surveys and closes them if closing time has arrived
        """
        # Fetch the list of all active surveys
        surveys = self._survey_repository.get_all_active_surveys()
        # If the list is empty or it doesn't exist, return
        if not surveys:
            return False
        if len(surveys) == 0:
            return False
        for survey in surveys:
            survey_id = survey.id
            survey_time_end = self._survey_repository.get_survey_time_end(survey_id)
            closing_time = time_to_close(survey_time_end)
            if closing_time:
                self._survey_repository.close_survey(survey_id)

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

    def get_choice_popularities(self, survey_id:str):
        """
        Calls repository function fetch_survey_responses() to get user rankings
        for the choices in the survey and from this data calculates how many
        times each choice has been ranked in top three choices.

        Returns a tuple. First element is number of answers and second is
        a dictionary where key is choice id and value number of times a choice
        has been valued in top three by a student

        Args:
            survey_id (str): the id of the survey
        """
        responses = self._survey_repository.fetch_survey_responses(survey_id)
        answers = len(responses)
        popularities = {}
        for response in responses:
            ranking = response[1].split(",")
            for i in range(min(3,len(ranking))):
                if int(ranking[i]) in popularities:
                    popularities[int(ranking[i])] += 1
                else:
                    popularities[int(ranking[i])] = 1
        return (answers, popularities)

    def validate_created_survey(self, survey_dict, edited = False):
        #print("VALIDATING")
        #print(survey_dict)

        # Name length
        if len(survey_dict["surveyGroupname"]) < 5:
            return {"success": False, "message": {"status":"0", "msg":"Kyselyn nimen tulee olla vähintään 5 merkkiä pitkä"}}
        
        # Min choices is a number
        if not edited:
            if not isinstance(survey_dict["minchoices"], int):
                return {"success": False, "message": {"status":"0", "msg":"Priorisoitavien ryhmien vähimmäismäärän tulee olla numero"}}

        return {"success": True}
    
    def save_survey_edit(self, survey_id, edit_dict, user_id):
        '''
        Function to save edited survey data
        Edit page might not return every data field for survey so function first
        gets survey data as dictionary and replaces applicaple fields with edited fields
        Then inputs data to service that saves edis
        args:
            survey_id (str): ID of the survey being edited
            edict_dict (dict): Dictionary of values returned by save edit
        '''
        surveyname = edit_dict["surveyGroupname"]

        name_changed = False
        name = self._survey_repository.get_survey(survey_id).surveyname
        if name != surveyname:
            name_changed = True
        if self._survey_repository.survey_name_exists(surveyname, user_id) and name_changed:
            message = "Tämän niminen kysely on jo käynnissä! Sulje se tai muuta nimeaä!"
            return (False, message)

        description = edit_dict["surveyInformation"]
        date_end = edit_dict["enddate"]
        time_end = edit_dict["endtime"]

        datetime_end = date_to_sql_valid(date_end) + " " +  time_end

        saved = self._survey_repository.save_survey_edit(survey_id, surveyname, description, datetime_end)

        # ADD FUNCTIONALITY FOR EDITING SURVEY CHOICES!

        if not saved:
            message = "Ei voitu tallentaa muutoksia tietokantaan!"
            return (False, message)
        message = "Muutokset tallennettu!"
        return (True, message)

    def update_survey_group_sizes(self, survey_id, choices):
        """
        Updates the group sizes of survey choices. A teacher only gets to use this fucntion if the amount of students that have answered the
        survey is greater than the sum of all group sizes.
        """
        count = 0
        for choice in choices:
            success = self._choices_repository.edit_choice_group_size(survey_id, choice['Nimi'], choice['Enimmäispaikat'])
            if not success:
                if count > 0:
                    message = "Häiriö. Osa ryhmäkoon päivityksistä ei onnistunut"
                    return (False, message)
                else:
                    message = "Häiriö. Ryhmäkokojen päivitys ei onnistunut"
                    return (False, message)
            count += 1
        message = "Ryhmäkoot päivitetty"
        return (True, message)
    
    def len_active_surveys(self):
        """
        Gets the size of all active surveys. Used for analytics in the admin page.
        """
        surveys = self._survey_repository.get_all_active_surveys()
        if not surveys:
            return 0
        return len(surveys)
    
    def len_all_surveys(self):
        """
        Gets the size of all surveys. Used for analytics in the admin page.
        """
        surveys = self._survey_repository.get_all_surveys()
        if not surveys:
            return 0
        return len(surveys)
    
    def get_all_active_surveys(self):
        """
        Gets the list of all active surveys. Used for analytics in the admin page.
        """
        surveys = self._survey_repository.get_all_active_survey_admin_data()
        if not surveys:
            return False
        admin_data = []
        for survey in surveys:
            survey_choices = default_survey_choices_repository.find_survey_choices(survey[0])
            survey_data = [survey[0], survey[1], survey[2], survey[3], survey[4], survey[5], len(survey_choices)]
            admin_data.append(survey_data)
        return admin_data

    def set_survey_deleted_true(self, survey_id):
        """
        Sets survey tables column deleted to true, doesn't actually delete the survey
        RETURNS whether updating was successful
        """
        return self._survey_repository.set_survey_deleted_true(survey_id)


survey_service = SurveyService()
