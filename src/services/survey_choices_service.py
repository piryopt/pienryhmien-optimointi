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

    def get_list_of_stage_survey_choices(self, survey_id: str, stage: str):
        """
        Returns a list of survey choices from a survey for a given stage

        args:
            survey_id: The id of the survey from which we want the survey choices
            stage: The stage of the survey choices
        """
        return self._survey_choices_repository.get_stage_choices(survey_id, stage)  

    def get_survey_choice(self, survey_choice_id: int):
        """
        Returns the data of a survey choice

        args:
            survey_choice_id: The id of the survey choice
        """
        survey_choice = self._survey_choices_repository.get_survey_choice(survey_choice_id)
        return dict(survey_choice._mapping) if survey_choice else None

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
        additional_infos = self._survey_choices_repository.get_choice_additional_infos(choice_id)
        return [dict(row._mapping) for row in additional_infos]

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

    def get_stages_available_spaces(self, survey_id):
        """
        Returns the total number of available space for each stage in the groups of a survey
        """
        spaces = {}
        stages = self._survey_repository.get_all_survey_stages(survey_id)
        for stage in stages:
            spaces[stage.stage] = self._survey_choices_repository.count_spaces_in_stage(survey_id, stage.stage)
        return spaces

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

    def add_multistage_choice(self, **kwargs):
        """
        Adds a new multistage choice (e.g., a recurring group) to a survey.

        Expected keyword arguments (**kwargs):
            survey_id (str): The ID of the survey the choice belongs to.
            name (str): The display name of the choice.
            max_spaces (int): Maximum number of participants allowed.
            min_size (int): Minimum number of participants required.
            stages (list[str]): A list of stage identifiers (e.g., ["week1", "week2"]).
            mandatory (bool): Whether the group is mandatory. Defaults to False.

        Returns:
            dict: A result dictionary with keys:
                - success (bool): True if creation succeeded.
                - message (str): Informational message.
        """
        try:
            required_fields = ["survey_id", "name", "max_spaces", "min_size", "mandatory", "stage", "order_number", "participation_limit"]
            choice_id = self._survey_choices_repository.create_new_multistage_choice(**kwargs)
            for key, val in kwargs.items():
                if key not in required_fields:
                    # no hidden field feature implemented yet
                    self._survey_choices_repository.create_new_choice_info(choice_id, key, val, False)
        except Exception as e:
            return {
                "success": False,
                "message": f"Unexpected service error: {e}"
            }

    def get_survey_choices_by_stage(self, survey_id):
        """
        Returns survey choices grouped by stage in structured form
        """
        rows = self._survey_choices_repository.get_choices_grouped_by_stage(survey_id)
        stages = []
        stageIndices = {}
        index = 0
        for row in rows:
            stage_id = row["stage"] or "no_stage"

            if stage_id not in stageIndices:
                stageIndices[stage_id] = index
                stages.append({
                    "name": stage_id,
                    "orderNumber": row["order_number"],
                    "hasMandatory": any(map(lambda r: r["mandatory"] if r["stage"] == stage_id else False, rows)),
                    "choices": []
                })
                index += 1
            choices = stages[stageIndices[stage_id]]["choices"]

            matching_choices = [c for c in choices if c["id"] == row["choice_id"]]
            choice = matching_choices[0] if matching_choices else None

            if not choice:
                choice = {
                    "id": row["choice_id"],
                    "name": row["choice_name"],
                    "slots": row["max_spaces"],
                    "min_size": row["min_size"],
                    "mandatory": row["mandatory"],
                    "participation_limit": row["participation_limit"],
                    "infos": []
                }
                choices.append(choice)

            if row.get("info_key"):
                choice["infos"].append({
                    row["info_key"]: row["info_value"],
                    "hidden": row["hidden"]
                })
        return sorted(stages, key=lambda s: s["orderNumber"])
    def set_choices_deleted_true(self, survey_id):
        """
        Sets choices of survey to deleted status. Returns boolean.

        Args:
            survey_id: id for the survey
        """
        return self._survey_choices_repository.set_choices_deleted_true(survey_id)


survey_choices_service = SurveyChoicesService()
