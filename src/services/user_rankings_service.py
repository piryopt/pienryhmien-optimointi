from src.repositories.user_rankings_repository import (
    user_rankings_repository as default_user_rankings_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class UserRankingsService:
    def __init__(self, user_rankings_repository = default_user_rankings_repository, survey_repository = default_survey_repository):
        """
        Initalized the service for user rankings with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            user_rankings_repository: The repository for user rankings
            survey_repository: The repository for surveys
        """
        self._user_rankings_repository = user_rankings_repository
        self._survey_repository = survey_repository

    def add_user_ranking(self, user_id, survey_id, ranking, rejections, reason):
        """
        Adds a user ranking

        args:
            user_id: The id of the user
            survey_id: The id of the survey
            ranking: The ranking of the survey by the user
            rejections: The rejections of the survey by the user. This can be an empty string if no rejections added
            reason: The reasoning for the rejections. This can be an empty string if no rejections added
        """
        ranking = self._user_rankings_repository.add_user_ranking(user_id,survey_id,ranking, rejections, reason)
        return ranking

    def user_ranking_exists(self, survey_id, user_id):
        """
        Check if a user ranking exists for a survey

        args:
            survey_id: The id of the survey
            user_id: The id of the user
        """
        ranking = self._user_rankings_repository.get_user_ranking(user_id, survey_id)
        if not ranking:
            return False
        return ranking

    def delete_ranking(self, survey_id, current_user_id):
        """
        Deletes the ranking for a survey

        args:
            survey_id: The id of the survey
            current_user_id: The id of the user
        """
        ranking = self._user_rankings_repository.get_user_ranking(current_user_id, survey_id)
        if not ranking:
            return False
        self._user_rankings_repository.delete_user_ranking(current_user_id, survey_id)
        return True

    def get_user_ranking(self, user_id, survey_id):
        """
        Gets the user ranking for a survey

        args:
            survey_id: The id of the survey
            user_id: The id of the user
        """
        ranking = self._user_rankings_repository.get_user_ranking(user_id, survey_id)
        return ranking.ranking

    def get_user_rejections(self, user_id, survey_id):
        """
        Gets the user rejections for a survey

        args:
            survey_id: The id of the survey
            user_id: The id of the user
        """
        ranking = self._user_rankings_repository.get_user_ranking(user_id, survey_id)
        return ranking.rejections
    
    def len_all_rankings(self):
        """
        Get the amount of all rankings made in Jakaja. Used for analytics in the admin page.
        """
        rankings = self._user_rankings_repository.get_all_rankings()
        if not rankings:
            return 0
        return len(rankings)

user_rankings_service = UserRankingsService()
