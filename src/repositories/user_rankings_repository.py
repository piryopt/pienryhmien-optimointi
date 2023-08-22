from sqlalchemy import text # pylint: disable=R0401
from src import db

class UserRankingsRepository:
    def add_user_ranking(self, user_id, survey_id, ranking, rejections, reason):
        """
        SQL code for adding a new entry into user_survey_rankings table

        args:
            user_id: The id of the user
            survey_id: The id of the survey
            ranking: The ranking of the user for the survey in question
            rejections: The rejections of the user for the survey in question
            reason: The reason of the user for the rejections of the survey in question
        """
        try:
            sql = """
                INSERT INTO user_survey_rankings (user_id, survey_id, ranking, rejections, reason, deleted) 
                VALUES (:user_id, :survey_id, :ranking, :rejections, :reason, :deleted) 
                ON CONFLICT (user_id, survey_id) 
                DO UPDATE SET ranking=:ranking, rejections=:rejections, reason=:reason, deleted=:deleted
                """
            db.session.execute(text(sql), {"user_id":user_id,"survey_id":survey_id,"ranking":ranking, "rejections":rejections, "reason":reason, "deleted":False})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_user_ranking(self, user_id, survey_id):
        """
        SQL code for getting all data from a user_survey_ranking entry

        args:
            user_id: The id of the user
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT * FROM user_survey_rankings WHERE (user_id=:user_id AND survey_id=:survey_id AND deleted=False)"
            result = db.session.execute(text(sql), {"user_id":user_id, "survey_id":survey_id})
            ranking = result.fetchone()
            if not ranking:
                return False
            return ranking
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def delete_user_ranking(self, user_id, survey_id):
        """
        SQL code for deleting a user_survey_ranking entry. It can be manually restored if no new ranking is added 

        args:
            user_id: The id of the user
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE user_survey_rankings SET deleted = True WHERE (user_id=:user_id AND survey_id=:survey_id)"
            db.session.execute(text(sql), {"user_id":user_id, "survey_id":survey_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

user_rankings_repository = UserRankingsRepository()
