from src.repositories.final_group_repository import (
    final_group_repository as default_final_group_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

from src.repositories.user_rankings_repository import (
    user_rankings_repository as default_user_rankings_repository
)


class FinalGroupService:
    def __init__(self, final_group_repository = default_final_group_repository,
                  survey_repository = default_survey_repository, user_rankings_repository = default_user_rankings_repository):
        """
        Initializes the the service with the different repositories. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            final_group_repository: The repository for final groups
            survey_repository: The repository for surveys
            user_rankings_repository: The repository for user rankings

        """
        self._final_group_repository = final_group_repository
        self._survey_repository = survey_repository
        self._user_rankings_repository = user_rankings_repository

    def save_result(self, user_id, survey_id, choice_id):
        """
        Saves the result of a survey for a user. Returns true or false depending on if it was a success

        args:
            user_id: The id of the user in question
            survey_id: The id of the survey in question
            choice_id: The id of the survey choice in question
        """
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            print("SURVEY DOES NOT EXIST!")
            return False
        ranking = self._user_rankings_repository.get_user_ranking(user_id, survey_id)
        if not ranking:
            print("USER RANKING FOR THIS USER DOES NOT EXIST!")
            return False
        saved = self._final_group_repository.save_result(user_id, survey_id, choice_id)
        return saved

final_group_service = FinalGroupService()
