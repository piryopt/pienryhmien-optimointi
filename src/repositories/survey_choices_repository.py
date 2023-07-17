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
            
    def create_new_survey_choice(self, survey_id, name, seats):
        '''
        Adds a new choice to existing survey, updates just survey_choices table
        RETURNS created choice's id
        '''
        try:
            sql = "INSERT INTO survey_choices (survey_id, name, max_spaces)"\
                " VALUES (:survey_id, :name, :max_spaces) RETURNING id"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "name":name, "max_spaces":seats})
            db.session.commit()
            return result.fetchone()[0]
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_choice_name_and_spaces(self, choice_id):
        try:
            sql = "SELECT name, max_spaces FROM survey_choices WHERE id=:id"
            result = db.session.execute(text(sql), {"id":choice_id})
            return result.fetchone()
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

survey_choices_repository = SurveyChoicesRepository()
