from app import db
from sqlalchemy import text

class SurveyRepository:
    def check_if_survey_exists(self, survey_id):
        try:
            sql = "SELECT id FROM surveys where id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            surveys = result.fetchall()
            if len(surveys) > 0:
                return True
            return False
        except:
            print("ERROR IN GETTING SURVEY!")
            return False

    def find_survey_choices(self, survey_id):
        try:
            sql = "SELECT id, name, info1, info2 FROM survey_choices WHERE survey_id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            survey_choices = result.fetchall()
            return survey_choices
        except:
            print("ERROR IN GETTING SURVEY CHOICES!")
            return False
        
    def new_user_ranking(self, user_id, survey_id, ranking):
        try:
            sql = "INSERT INTO user_survey_rankings (user_id, survey_id, ranking, deleted) VALUES (:user_id, :survey_id, :ranking, :deleted)"
            db.session.execute(text(sql), {"user_id":user_id, "survey_id":survey_id, "ranking":ranking, "deleted":False})
            db.session.commit()
            return True
        except:
            print("ERROR WHILE ADDING A NEW USER RANKING!")
            return False

survey_repository = SurveyRepository()