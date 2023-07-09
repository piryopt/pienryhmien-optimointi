from sqlalchemy import text
from src import db
from src.repositories.user_repository import user_repository

class SurveyRepository:
    def check_if_survey_exists(self, survey_id):
        try:
            sql = "SELECT * FROM surveys WHERE id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            survey = result.fetchone()
            if not survey:
                return False
            return survey
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def find_survey_choices(self, survey_id):
        try:
            sql = "SELECT * FROM survey_choices WHERE survey_id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id})
            survey_choices = result.fetchall()
            return survey_choices
        except Exception as e: # pylint: disable=W0718
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
        except Exception as e: # pylint: disable=W0718
            print(e)

    def get_user_ranking(self, user_id, survey_id):
        try:
            sql = "SELECT * FROM user_survey_rankings WHERE (survey_id=:survey_id AND user_id=:user_id AND deleted=False)"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "user_id":user_id})
            ranking = result.fetchone()
            if not ranking:
                return False
            return ranking
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def delete_user_ranking(self, user_id, survey_id):
        try:
            sql = "UPDATE user_survey_rankings SET deleted = True WHERE (survey_id=:survey_id and user_id=:user_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "user_id":user_id})
            db.session.commit()
            return True
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

    def add_new_survey(self, surveyname):
        try:
            sql = "INSERT INTO surveys (surveyname, min_choices, closed) VALUES (:surveyname, :min_choices, :closed) RETURNING id"
            result = db.session.execute(text(sql), {"surveyname":surveyname, "min_choices":10, "closed":False})
            db.session.commit()
            survey = result.fetchone()[0]
            if not survey:
                return False
            return survey
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def survey_name_exists(self, surveyname):
        try:
            sql = "SELECT id FROM surveys WHERE surveyname=:surveyname"
            result = db.session.execute(text(sql), {"surveyname":surveyname})
            survey = result.fetchone()
            if not survey:
                return False
            return True
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
        

    # new functions for new schema

    def create_new_survey(self, surveyname, min_choices =1):
        '''
        Creates a new survey, updates just surveys table
        RETURNS created survey's id
        '''

        teacher_id = user_repository.get_user_id()
        sql = "INSERT INTO surveys (surveyname, teacher_id, min_choices, closed)"\
            " VALUES (:surveyname, :teacher_id, :min_choices, :closed) RETURNING id"
        result = db.session.execute(text(sql), {"surveyname":surveyname, "teacher_id":teacher_id, "min_choices":min_choices, "closed":False})
        db.session.commit()
        return result.fetchone()[0]

    def create_new_survey_choice(self, survey_id, name, seats):
        '''
        Adds a new choice to existing survey, updates just survey_choices table
        RETURNS created choice's id
        '''
        sql = "INSERT INTO survey_choices (survey_id, name, max_spaces)"\
              " VALUES (:survey_id, :name, :max_spaces) RETURNING id"
        result = db.session.execute(text(sql), {"survey_id":survey_id, "name":name, "max_spaces":seats})
        db.session.commit()
        return result.fetchone()[0]

    def create_new_choice_info(self, choice_id, info_key, info_value):
        '''
        Adds an additional to existing survey choice, updates choice_infos table
        '''
        sql = "INSERT INTO choice_infos (choice_id, info_key, info_value)"\
              " VALUES (:c_id, :i_key, :i_value)"
        result = db.session.execute(text(sql), {"c_id":choice_id, "i_key":info_key, "i_value":info_value})
        db.session.commit()


survey_repository = SurveyRepository()
