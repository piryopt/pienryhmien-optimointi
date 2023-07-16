from sqlalchemy import text
from src import db

class SurveyChoicesRepository:
    def find_survey_choices(self, survey_id):
            try:
                sql = "SELECT * FROM survey_choices WHERE survey_id=:survey_id"
                result = db.session.execute(text(sql), {"survey_id":survey_id})
                survey_choices = result.fetchall()
                return survey_choices
            except Exception as e: # pylint: disable=W0718
                print(e)
                return False
            
    def get_survey_choice(self, id):
            try:
                sql = "SELECT * FROM survey_choices WHERE id=:id"
                result = db.session.execute(text(sql), {"id":id})
                ranking = result.fetchone()
                if not ranking:
                    return False
                return ranking
            except Exception as e: # pylint: disable=W0718
                print(e)
                return False
            
    def add_new_survey_choice(self, survey_id, name, max_spaces, info1, info2):
            try:
                sql = """
                    INSERT INTO survey_choices (survey_id, name, max_spaces, info1, info2)
                    VALUES (:survey_id, :name, :max_spaces, :info1, :info2)
                    """
                db.session.execute(text(sql), {"survey_id":survey_id, "name":name, "max_spaces":max_spaces, "info1":info1, "info2":info2})
                db.session.commit()
                return True
            except Exception as e: # pylint: disable=W0718
                print(e)
                return False

survey_choices_repository = SurveyChoicesRepository()
