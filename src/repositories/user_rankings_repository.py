from sqlalchemy import text # pylint: disable=R0401
from src import db

class UserRankingsRepository:
    def add_user_ranking(self, user_id, survey_id, ranking, rejections, reason):
        try:
            sql = """
                INSERT INTO user_survey_rankings (user_id, survey_id, ranking, rejections, reason, deleted) 
                VALUES (:user_id, :survey_id, :ranking, :rejections, :reason, :deleted) 
                ON CONFLICT (user_id, survey_id) 
                DO UPDATE SET ranking=:ranking, rejections=:rejections, reason=:reason, deleted=:deleted
                """
            db.session.execute(text(sql), {"user_id":user_id,"survey_id":survey_id,"ranking":ranking, "rejections":rejections, "reason":reason, "deleted":False})
            db.session.commit()
        except Exception as e: # pylint: disable=W0718
            print(e)

    def get_user_ranking(self, user_id, survey_id):
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
        try:
            sql = "UPDATE user_survey_rankings SET deleted = True WHERE (user_id=:user_id AND survey_id=survey_id)"
            db.session.execute(text(sql), {"user_id":user_id, "survey_id":survey_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

user_rankings_repository = UserRankingsRepository()
