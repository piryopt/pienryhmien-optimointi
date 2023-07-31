from src.repositories.user_rankings_repository import (
    user_rankings_repository as default_user_rankings_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class UserRankingsService:
    def __init__(self, user_rankings_repository = default_user_rankings_repository, survey_repository = default_survey_repository):
        self._user_rankings_repository = user_rankings_repository
        self._survey_repository = survey_repository

    def add_user_ranking(self, user_id, survey_id, ranking, rejections, reason):
        self._user_rankings_repository.add_user_ranking(user_id,survey_id,ranking, rejections, reason)
        return True

    def user_ranking_exists(self, survey_id, user_id):
        ranking = self._user_rankings_repository.get_user_ranking(user_id, survey_id)
        if not ranking:
            return False
        return ranking

    def delete_ranking(self, survey_id, current_user_id):
        ranking = self._user_rankings_repository.get_user_ranking(current_user_id, survey_id)
        if not ranking:
            print("NO RANKING FOR THIS SURVEY!")
            return False
        self._user_rankings_repository.delete_user_ranking(current_user_id, survey_id)
        return True

    def get_user_ranking(self, user_id, survey_id):
        ranking = self._user_rankings_repository.get_user_ranking(user_id, survey_id)
        if not ranking:
            print("No ranking for this user!")
        return ranking.ranking

user_rankings_service = UserRankingsService()
