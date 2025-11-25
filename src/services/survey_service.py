from datetime import datetime, timedelta
from flask_babel import gettext
from flask import session
from src.repositories.survey_repository import survey_repository as default_survey_repository
from src.repositories.survey_owners_repository import survey_owners_repository as default_survey_owners_repository
from src.repositories.survey_choices_repository import survey_choices_repository as default_survey_choices_repository
from src.services.user_service import user_service as default_user_service
from src.services.user_rankings_service import user_rankings_service as default_user_rankings_service
from src.tools.parsers import parser_csv_to_dict, parser_dict_to_survey, parser_existing_survey_to_dict
from src.tools.date_converter import time_to_close, format_datestring
from src.tools.parsers import date_to_sql_valid
from src.tools.constants import SURVEY_FIELDS


class SurveyService:
    SURVEY_FIELDS = SURVEY_FIELDS

    def __init__(
        self,
        survey_repositroy=default_survey_repository,
        survey_owners_repository=default_survey_owners_repository,
        choices_repository=default_survey_choices_repository,
        user_service=default_user_service,
    ):
        """
        Initalizes the service for surveys with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            SURVEY_FIELDS: Survey column names to help with languages
            survey_repository: The repository for surveys
            survey_owners_repository: The repository for survey owners
            choices_repository: The repository for survey choices
            user_service: The service for users


        """
        self._survey_repository = survey_repositroy
        self._survey_owners_repository = survey_owners_repository
        self._choices_repository = choices_repository
        self._user_service = user_service

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
        return survey.surveyname

    def is_multistage(self, survey_id):
        """
        Returns True if the survey has stages (is multistage), False otherwise.

        args:
            survey_id: The id of the survey
        """
        result = self._survey_repository.is_multistage(survey_id)
        if not result:
            return False
        return result

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
        admin = self._user_service.check_if_admin(user_id)
        if not owner_exists and not admin:
            return False
        return self._survey_repository.close_survey(survey_id)

    def open_survey(self, survey_id, user_id, new_end_time):
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
        admin = self._user_service.check_if_admin(user_id)
        if not owner_exists and not admin:
            return False
        if self._survey_repository.survey_name_exists(survey.surveyname, user_id):
            return False
        if not self._choices_repository.remove_empty_choices(survey_id):
            return False
        return self._survey_repository.open_survey(survey_id, new_end_time)

    def get_active_surveys(self, user_id):
        """
        Get the list of active surveys for a user

        args:
            user_id: The id of the user whose active surveys we want
        """
        surveys = self._survey_repository.get_active_surveys(user_id)
        return [{key: format_datestring(val) if key == "time_end" else val for key, val in survey._mapping.items()} for survey in surveys]

    def get_active_surveys_and_response_count(self, user_id):
        """
        Get the active surveys for a user and response count

        args:
            user_id: The id of the user whose active surveys we want
        """

        surveys = self._survey_repository.get_active_surveys_and_response_count(user_id)
        return [{key: format_datestring(val) if key == "time_end" else val for key, val in survey._mapping.items()} for survey in surveys]

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
        return [{key: format_datestring(val) if key == "time_end" else val for key, val in survey._mapping.items()} for survey in surveys]

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
        """
        Calls tools.parsers csv to dict parser
        RETURNS the dictionary
        """
        return parser_csv_to_dict(file)  # in tools

    def create_new_survey_manual(
        self,
        survey_choices,
        survey_name,
        user_id,
        description,
        minchoices,
        date_end,
        time_end,
        allowed_denied_choices=0,
        allow_search_visibility=True,
    ):
        """
        Calls tools.parsers dictionary to survey parser
        that creates the survey, its choices and their additional infos
        RETURNS created survey's id
        """
        if self._survey_repository.survey_name_exists(survey_name, user_id):
            return False

        return parser_dict_to_survey(
            survey_choices, survey_name, description, minchoices, date_end, time_end, allowed_denied_choices, allow_search_visibility
        )

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
        """
        Gets survey, its choices and their additional infos as dictionary
        RETURNS dictionary
        """
        return parser_existing_survey_to_dict(survey_id)

    def get_list_active_answered(self, user_id):
        """
        Gets a list of active surveys that the user has answered.

        args:
            user_id: The id of the user
        """
        return self._survey_repository.get_list_active_answered(user_id)

    def get_list_closed_answered(self, user_id):
        """
        Gets a list of closed surveys that the user has answered.

        args:
            user_id: The id of the user
        """
        return self._survey_repository.get_list_closed_answered(user_id)

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

    def check_for_surveys_to_delete(self):
        """
        Gets a list of all surveys and deletes them and their related data if end time was over two years ago.
        """

        surveys = self._survey_repository.get_all_active_surveys()

        for survey in surveys:
            if survey.time_end <= datetime.now() - timedelta(days=365 * 2):
                self._survey_repository.delete_survey_permanently(survey.id)

    def check_for_trashed_surveys_to_delete(self):
        """
        Gets a list of all surveys and deletes them and their related data if survey has been in trash bin for a week.
        """

        surveys = self._survey_repository.get_all_deleted_surveys()

        for survey in surveys:
            if survey.deleted_at <= datetime.now() - timedelta(days=7):
                self._survey_repository.delete_survey_permanently(survey.id)

    def delete_survey_permanently(self, survey_id):
        """
        Deletes survey and all related data permanently.

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.delete_survey_permanently(survey_id)

    def fetch_survey_responses(self, survey_id):
        """
        Gets a list of user_survey_rankings for the survey

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.fetch_survey_responses(survey_id)

    def fetch_survey_responses_grouped_by_stages(self, survey_id):
        """
        Gets a list of user_survey_rankings for the survey grouped by stage

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.fetch_survey_responses_grouped_by_stages(survey_id)

    def fetch_survey_responses_grouped_by_stage(self, survey_id):
        """
        Gets a list of user_survey_rankings for the survey grouped by stage

        args:
            survey_id: The id of the survey
        """
        return self._survey_repository.fetch_survey_response_grouped_by_stages(survey_id)

    def get_choice_popularities(self, survey_id: str):
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
            for i in range(min(3, len(ranking))):
                if int(ranking[i]) in popularities:
                    popularities[int(ranking[i])] += 1
                else:
                    popularities[int(ranking[i])] = 1
        return (answers, popularities)

    def validate_created_survey(self, survey_dict, edited=False, multistage=False):
        survey_name = survey_dict.get("surveyGroupname", "")
        description = survey_dict.get("surveyInformation", "")
        survey_choices = survey_dict.get("choices", [])
        min_choices_map = survey_dict.get("minChoicesPerStage", {}) if multistage else survey_dict.get("minchoices", 0)
        date_end = survey_dict.get("enddate", "")
        time_end = survey_dict.get("endtime", "")
        allowed_denied_choices = survey_dict.get("allowedDeniedChoices", 0)
        allow_search_visibility = survey_dict.get("allowSearchVisibility", False)

        date_string = f"{date_end} {time_end}"
        format_code = "%d.%m.%Y %H:%M"
        try:
            parsed_time = datetime.strptime(date_string, format_code)
        except Exception:
            return {"success": False, "message": "Invalid date/time format"}

        if parsed_time <= datetime.now():
            msg = "Response period's end can't be in the past"
            return {"success": False, "message": msg}

        if not isinstance(allowed_denied_choices, int):
            msg = "Survey denied choices must be an integer"
            return {"success": False, "message": msg}

        if not isinstance(allow_search_visibility, bool):
            msg = "Survey search visibility must be a boolean"
            return {"success": False, "message": msg}

        if len(survey_name) < 5:
            msg = "Survey name must be atleast 5 characters long"
            return {"success": False, "message": msg}

        if not isinstance(description, str):
            msg = "Survey description must be a string"
            return {"success": False, "message": msg}

        # Min choices is a number
        if not edited:
            if not multistage:
                if not isinstance(min_choices_map, int):
                    msg = "The minimum number of prioritized groups should be a number!"
                    return {"success": False, "message": msg}

            else:
                if not isinstance(min_choices_map, dict):
                    msg = "Per-stage minimum choices must be provided as an object/dictionary!"
                    return {"success": False, "message": msg}

                for v in min_choices_map.values():
                    if not isinstance(v, int):
                        msg = "Each per-stage minimum number of prioritized groups should be a number!"
                        return {"success": False, "message": msg}

        if not multistage and (min_choices_map > len(survey_choices)):
            msg = "There are less choices than the minimum amount of prioritized groups!"
            return {"success": False, "message": msg}

        if "choices" in survey_dict:
            for choice in survey_dict["choices"]:
                result = self.validate_survey_choice(choice)
                if not result["success"]:
                    return result
        elif multistage:
            stage_names = [s.get("name", "") for s in survey_dict["stages"]]
            if len(stage_names) != len(set(stage_names)):
                return {"success": False, "message": "Name of every stage must be unique within a survey"}
            for stage in survey_dict["stages"]:
                stage_name = (stage.get("name") or "").strip()
                if stage_name == "":
                    return {"success": False, "message": "Every stage must have a non-empty name"}
                if stage_name not in min_choices_map:
                    print("stage name:", stage_name)
                    print("min choices per stages:", min_choices_map)
                    return {"success": False, "message": f"Missing minchoices entry for stage '{stage_name}'"}
                required_min = min_choices_map.get(stage_name, 0)
                if len(stage.get("choices", [])) < required_min:
                    msg = "There are less choices than the minimum amount of prioritized groups!"
                    return {"success": False, "message": msg}

                for choice in stage.get("choices", []):
                    result = self.validate_survey_choice(choice)
                    if not result["success"]:
                        return result
        return {"success": True}

    def validate_survey_choice(self, choice):
        """
        method for validating a survey choice
        """
        if len(choice["name"]) < 5:
            msg = "Group requires a name that is at least 5 characters long"
            return {"success": False, "message": msg}
        if not isinstance(choice["mandatory"], bool):
            msg = "Group mandatory must be a boolean"
            return {"success": False, "message": msg}
        if choice["min_size"] > choice["max_spaces"]:
            msg = "Group minimum size must be smaller than maximum size"
            return {"success": False, "message": msg}

        return {"success": True}

    def save_survey_edit(self, survey_id, edit_dict, user_id):
        """
        Function to save edited survey data
        Edit page might not return every data field for survey so function first
        gets survey data as dictionary and replaces applicaple fields with edited fields
        Then inputs data to service that saves edis
        args:
            survey_id (str): ID of the survey being edited
            edict_dict (dict): Dictionary of values returned by save edit
        """
        surveyname = edit_dict["surveyGroupname"]

        name_changed = False
        name = self._survey_repository.get_survey(survey_id).surveyname
        if name != surveyname:
            name_changed = True
        if self._survey_repository.survey_name_exists(surveyname, user_id) and name_changed:
            message = gettext("Tämän niminen kysely on jo käynnissä! Sulje se tai muuta nimeaä!")
            return (False, message)

        description = edit_dict["surveyInformation"]
        date_end = edit_dict["enddate"]
        time_end = edit_dict["endtime"]

        date_string = f"{date_end} {time_end}"
        format_code = "%d.%m.%Y %H:%M"

        parsed_time = datetime.strptime(date_string, format_code)

        if parsed_time <= datetime.now():
            message = gettext("Vastausajan päättyminen ei voi olla menneisyydessä")
            return (False, message)

        datetime_end = date_to_sql_valid(date_end) + " " + time_end

        saved = self._survey_repository.save_survey_edit(survey_id, surveyname, description, datetime_end)

        # ADD FUNCTIONALITY FOR EDITING SURVEY CHOICES!

        if not saved:
            message = gettext("Ei voitu tallentaa muutoksia tietokantaan!")
            return (False, message)
        message = gettext("Muutokset tallennettu!")
        return (True, message)

    def update_survey_group_sizes(self, survey_id, choices):
        """
        Updates the group sizes of survey choices. A teacher only gets to use this
        fucntion if the amount of students that have answered the survey is greater
        than the sum of all group sizes.
        """
        count = 0
        language = session.get("language", "fi")
        for choice in choices:
            # new behavior with choice IDs and max_spaces key also supports old behavior
            if "id" in choice and ("max_spaces" in choice or "maxSpaces" in choice):
                seats = choice.get("max_spaces") if "max_spaces" in choice else choice.get("maxSpaces")
                try:
                    seats_int = int(seats)
                except Exception:
                    seats_int = 0
                success = self._choices_repository.edit_choice_group_size_by_id(choice["id"], seats_int)
            else:
                # legacy behavior expects localized keys for name and spaces
                try:
                    name_key = SurveyService.SURVEY_FIELDS["name"][language]
                    spaces_key = SurveyService.SURVEY_FIELDS["spaces"][language]
                    seats_val = choice[spaces_key]
                    seats_int = int(seats_val)
                except Exception:
                    seats_int = 0
                success = self._choices_repository.edit_choice_group_size(survey_id, choice.get(name_key, ""), seats_int)
            if not success:
                if count > 0:
                    message = gettext("Häiriö. Osa ryhmäkoon päivityksistä ei onnistunut")
                    return (False, message)
                else:
                    message = gettext("Häiriö. Ryhmäkokojen päivitys ei onnistunut")
                    return (False, message)
            count += 1
        message = gettext("Ryhmäkoot päivitetty")
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
        return len(surveys)

    def get_all_active_surveys(self):
        """
        Gets the list of all active surveys. Used for analytics in the admin page.
        """
        surveys = self._survey_repository.get_all_active_surveys()
        if not surveys:
            return []
        admin_data = []
        for survey in surveys:
            survey_choices = default_survey_choices_repository.find_survey_choices(survey.id)
            survey_data = [
                survey.id,
                survey.surveyname,
                survey.min_choices,
                survey.time_end,
                survey.allowed_denied_choices,
                survey.allow_search_visibility,
                len(survey_choices),
            ]
            admin_data.append(survey_data)
        return admin_data

    def get_admin_analytics(self):
        """
        Collect analytics numbers used in admin UI.
        Returns a dict with named metrics or None on error
        Keys:
        {
            "total_surveys": int,      # total number of surveys in system
            "active_surveys": int,     # number of active (open) surveys
            "total_students": int,     # number of registered students
            "total_responses": int,    # total rankings/responses created
            "total_teachers": int      # number of registered teachers
        }
        """
        try:
            statistics = self._survey_repository.get_admintools_statistics()
            return {
                "total_surveys": statistics.total_created_surveys,
                "active_surveys": statistics.active_surveys_count,
                "total_students": statistics.registered_students_count,
                "total_responses": statistics.total_survey_answers,
                "total_teachers": statistics.registered_teachers_count
            }
        except Exception as e:
            print("Error collecting admin analytics:", e)
            return None

    def set_survey_deleted_true(self, survey_id):
        """
        Sets survey and choices tables column deleted to true, doesn't actually 
        delete the survey or choices. Also closes the survey. 
        RETURNS whether updating was successful
        """
        if not self.check_if_survey_closed(survey_id):
            self._survey_repository.close_survey(survey_id)
        self._choices_repository.set_choices_deleted_true(survey_id)
        return self._survey_repository.set_survey_deleted_true(survey_id)

    def set_survey_deleted_false(self, survey_id):
        """
        Sets survey tables column deleted to false
        RETURNS whether updating was successful
        """
        self._choices_repository.set_choices_deleted_false(survey_id)
        return self._survey_repository.set_survey_deleted_false(survey_id)

    def create_new_multiphase_survey(self, **kwargs):
        if self._survey_repository.survey_name_exists(kwargs["surveyname"], kwargs["user_id"]):
            return None

        survey_id = self._survey_repository.create_new_survey(**kwargs)
        return survey_id

    def get_all_survey_stages(self, survey_id):
        return self._survey_repository.get_all_survey_stages(survey_id)

    def get_trash_count(self, user_id):
        return self._survey_repository.get_trash_count(user_id)

    def get_list_deleted_surveys(self, user_id):
        """
        Get the list of set to be deleted surveys for a user

        args:
            user_id: The id of the user whose set to be deleted surveys we want
        """
        surveys = self._survey_repository.get_deleted_surveys(user_id)
        return [{key: format_datestring(val) if key == "time_end" else val for key, val in survey._mapping.items()} for survey in surveys]

    def save_statistics(self):
        """
        Saves old statistics
        """
        self._survey_repository.save_statistics()

survey_service = SurveyService()
