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

    def get_survey_choice(self, choice_id):
        try:
            sql = "SELECT * FROM survey_choices WHERE id=:id"
            result = db.session.execute(text(sql), {"id":choice_id})
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

    def create_new_choice_info(self, choice_id, info_key, info_value):
        '''
        Adds an additional to existing survey choice, updates choice_infos table
        '''
        try:
            sql = "INSERT INTO choice_infos (choice_id, info_key, info_value)"\
                " VALUES (:c_id, :i_key, :i_value)"
            db.session.execute(text(sql), {"c_id":choice_id, "i_key":info_key, "i_value":info_value})
            db.session.commit()
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_choice_additional_infos(self, choice_id):
        '''
        Gets a list of key-value pairs based on choice_id from choice_infos tables
        '''
        try:
            sql = "SELECT info_key, info_value FROM choice_infos WHERE choice_id=:choice_id"
            result = db.session.execute(text(sql), {"choice_id":choice_id})
            return result.fetchall()
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

survey_choices_repository = SurveyChoicesRepository()
