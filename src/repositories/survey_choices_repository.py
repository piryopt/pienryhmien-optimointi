from sqlalchemy import text
from src import db

class SurveyChoicesRepository:
    def find_survey_choices(self, survey_id):
        """
        SQL code for getting all survey choices for a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT * FROM survey_choices WHERE (survey_id=:survey_id AND deleted=False)"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            survey_choices = result.fetchall()
            return survey_choices
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_survey_choice(self, choice_id):
        """
        SQL code for getting all data from a survey choice

        args:
            choice_id: The id of the survey choice
        """
        try:
            sql = "SELECT * FROM survey_choices WHERE (id=:id AND deleted=False)"
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
            sql = "INSERT INTO survey_choices (survey_id, name, max_spaces, deleted)"\
                " VALUES (:survey_id, :name, :max_spaces, False) RETURNING id"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "name":name, "max_spaces":seats})
            db.session.commit()
            return result.fetchone()[0]
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def edit_choice_group_size(self, survey_id:str, choice_name:str, seats:int):
        '''
        Takes survey id, choice name and number of seats, updates this number of
        seats to the choice. (Choice id would be ideal but it's not used on the form)
        RETURNS True if managed, False if there's an error
        '''
        try:
            sql = "UPDATE survey_choices SET max_spaces = :max_spaces WHERE survey_id = :survey_id AND name = :choice_name"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "choice_name":choice_name, "max_spaces":seats})
            db.session.commit()
            return True
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
            return True
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

    def get_all_additional_infos(self, survey_id):
        '''
        Gets a list of all additional info on choices in a single survey.
        '''
        try:
            sql = """
                SELECT I.choice_id, I.info_key, I.info_value
                FROM choice_infos I JOIN survey_choices S
                ON I.choice_id = S.id
                WHERE (S.survey_id =:survey_id AND S.deleted = False)
                """
            result = db.session.execute(text(sql), {"survey_id": survey_id})
            return result.fetchall()
        except Exception as e:
            print(e)
            return False

survey_choices_repository = SurveyChoicesRepository()
