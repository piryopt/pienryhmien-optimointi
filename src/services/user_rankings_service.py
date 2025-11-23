from src.repositories.user_rankings_repository import user_rankings_repository as default_user_rankings_repository
from src.repositories.survey_repository import survey_repository as default_survey_repository


class UserRankingsService:
    def __init__(self, user_rankings_repository=default_user_rankings_repository, survey_repository=default_survey_repository):
        """
        Initalized the service for user rankings with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            user_rankings_repository: The repository for user rankings
            survey_repository: The repository for surveys
        """
        self._user_rankings_repository = user_rankings_repository
        self._survey_repository = survey_repository

    def add_user_ranking(self, user_id, survey_id, ranking, rejections, reason, **kwargs):
        """
        Adds a user ranking to the database.
    
        Args:
            user_id (int): The ID of the user submitting the ranking.
            survey_id (str): The ID of the survey being ranked.
            ranking (str): The ranking of the survey choices by the user (e.g., "1,2,3,4").
            rejections (str): The rejected survey choices (comma-separated string). 
                              Can be an empty string if no rejections are provided.
            reason (str): The reasoning or justification for the ranking or rejections. 
                          Can be an empty string if no reason is provided.
            **kwargs: Optional keyword arguments. Supported keys:
                - multistage_ranking (bool): Whether this ranking belongs to a multistage survey.
        """
        multistage_ranking = kwargs.get("multistage_ranking", False)
        ranking_exists = kwargs.get("ranking_exists", False)

        if multistage_ranking:
            ranking = self._user_rankings_repository.add_multistage_user_ranking(
                user_id, survey_id, ranking, rejections, reason, kwargs["stage"], kwargs["not_available"], ranking_exists
            )
        else:
            ranking = self._user_rankings_repository.add_user_ranking(
                user_id, survey_id, ranking, rejections, reason, ranking_exists
            )
    
        return ranking

    def user_ranking_exists(self, survey_id, user_id):
        """
        Check if a user ranking exists for a survey

        args:
            survey_id: The id of the survey
            user_id: The id of the user
        """
        return self._user_rankings_repository.get_user_ranking(user_id, survey_id)

    def user_ranking_exists_fast(self, survey_id, user_id):
        """
        Check if a user ranking exists for a survey. Returns boolean instead of the ranking.
        Should be more efficient than user_ranking_exists function
        """
        return self._user_rankings_repository.user_ranking_exists(user_id, survey_id)

    def get_user_multistage_rankings(self, survey_id, user_id):
        """
        Returns user's rankings grouped by stage for a multistage survey.
        """
        rows = self._user_rankings_repository.get_user_multistage_rankings(survey_id, user_id)
        if not rows:
            return None

        stages = {}
        for row in rows:
            stage_name = row.stage
            stages[stage_name] = {
                "ranking": row.ranking,
                "rejections": row.rejections,
                "reason": row.reason,
                "not_available": row.not_available
            }

        return stages

    def get_user_multistage_rankings_by_stage(self, survey_id, user_id, stage):
        """
        Returns user's rankings for a stage of a multistage survey
        """
        return self._user_rankings_repository.get_user_multistage_rankings_by_stage(survey_id, user_id, stage)

    def get_multistage_rankings_by_stage(self, survey_id, stage):
        return self._user_rankings_repository.get_all_rankings_by_stage(survey_id, stage)

    def delete_ranking(self, survey_id, current_user_id):
        """
        Deletes the ranking for a survey

        args:
            survey_id: The id of the survey
            current_user_id: The id of the user
        """
        ranking = self._user_rankings_repository.user_ranking_exists(current_user_id, survey_id)
        if not ranking:
            return False
        return self._user_rankings_repository.delete_user_ranking(current_user_id, survey_id)

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
        return self._user_rankings_repository.get_all_rankings()
        


user_rankings_service = UserRankingsService()
