from sqlalchemy import text
from app import db

class SurveyRepository:
    def check_if_survey_exists(self, survey_id):
        try:
            sql = "SELECT * FROM surveys WHERE id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            survey = result.fetchone()
            if not survey:
                return False
            return survey
        except Exception as e:
            print(e)
            return False

    def find_survey_choices(self, survey_id):
        try:
            sql = "SELECT id, name, info1, info2 FROM survey_choices WHERE survey_id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            survey_choices = result.fetchall()
            return survey_choices
        except Exception as e:
            print(e)
            return False

    def new_user_ranking(self, user_id, survey_id, ranking):
        try:
            sql = "INSERT INTO user_survey_rankings (user_id, survey_id, ranking, deleted) VALUES (:user_id, :survey_id, :ranking, :deleted)"
            db.session.execute(text(sql), {"user_id":user_id, "survey_id":survey_id, "ranking":ranking, "deleted":False})
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_user_ranking(self, user_id, survey_id):
        try:
            sql = "SELECT * FROM user_survey_rankings WHERE (survey_id=:survey_id AND user_id=:user_id AND deleted=False)"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "user_id":user_id})
            ranking = result.fetchone()
            if not ranking:
                return False
            return ranking
        except Exception as e:
            print(e)
            return False

    def delete_user_ranking(self, user_id, survey_id):
        try:
            sql = "UPDATE user_survey_rankings SET deleted = True WHERE (survey_id=:survey_id and user_id=:user_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "user_id":user_id})
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def get_survey_choice(self, id):
        try:
            sql = "SELECT id, name, info1, info2 FROM survey_choices WHERE id=:id"
            result = db.session.execute(text(sql), {"id":id})
            ranking = result.fetchone()
            if not ranking:
                return False
            return ranking
        except Exception as e:
            print(e)
            return False

    def add_user_ranking(self,user_id,survey_id,ranking):
        try:
            sql = """
                INSERT INTO user_survey_rankings (user_id, survey_id, ranking, deleted) 
                VALUES (:user_id, :survey_id, :ranking, :deleted) 
                ON CONFLICT (user_id, survey_id) 
                DO UPDATE SET ranking=:ranking, deleted=:deleted
                """
            db.session.execute(text(sql), {"user_id":user_id,"survey_id":survey_id,"ranking":ranking, "deleted":False})
            db.session.commit()
        except Exception as e:
            print(e)

survey_repository = SurveyRepository()
