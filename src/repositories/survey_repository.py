from sqlalchemy import text
from src import db

class SurveyRepository:
    def get_survey(self, survey_id):
        """
        SQL code for getting all data from a survey

        args:
            survey_id: The id of the survey
        """
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

    def survey_name_exists(self, surveyname, teacher_id):
        """
        SQL code for getting the id from a survey that has a certain name, is open and created by a certain user.

        args:
            surveyname: The name of the survey
            teacher_id: The id of the user
        """
        try:
            sql = "SELECT id FROM surveys WHERE (surveyname=:surveyname AND teacher_id=:teacher_id AND closed=False)"
            result = db.session.execute(text(sql), {"surveyname":surveyname, "teacher_id":teacher_id})
            survey = result.fetchone()
            if not survey:
                return False
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def count_created_surveys(self, user_id):
        """
        SQL code for getting the length of created surveys

        args:
            user_id: The id of the user
        """
        # Do we want to diplay all surveys created or only the active ones?
        try:
            sql = "SELECT * FROM surveys WHERE teacher_id=:user_id"
            result = db.session.execute(text(sql), {"user_id":user_id})
            survey_list = result.fetchall()
            if not survey_list:
                return False
            return len(survey_list)
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def close_survey(self, survey_id, teacher_id):
        """
        SQL code for closing a survey

        args:
            survey_id: The id of the survey
            teacher_id: The id of the user
        """
        try:
            sql = "UPDATE surveys SET closed = True WHERE (id=:survey_id and teacher_id=:teacher_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "teacher_id":teacher_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def open_survey(self, survey_id, teacher_id):
        """
        SQL code for opening a survey

        args:
            survey_id: The id of the survey
            teacher_id: The id of the user
        """
        try:
            sql = "UPDATE surveys SET closed = False WHERE (id=:survey_id and teacher_id=:teacher_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "teacher_id":teacher_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_active_surveys(self, teacher_id):
        """
        SQL code getting the list of all active surveys created by a user.

        args:
            teacher_id: The id of the user
        """
        try:
            sql = "SELECT id, surveyname FROM surveys WHERE (teacher_id=:teacher_id AND closed=False)"
            result = db.session.execute(text(sql), {"teacher_id":teacher_id})
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_closed_surveys(self, teacher_id):
        """
        SQL code getting the list of all closed surveys created by a user.

        args:
            teacher_id: The id of the user
        """
        try:
            sql = "SELECT id, surveyname, closed, results_saved, time_end FROM surveys WHERE (teacher_id=:teacher_id AND closed=True) ORDER BY id ASC"
            result = db.session.execute(text(sql), {"teacher_id":teacher_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def update_survey_answered(self, survey_id):
        """
        SQL code for updating result_saved of the surveys table from False to True

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET results_saved = True WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id":survey_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def create_new_survey(self, surveyname, user_id, min_choices, description, begindate, enddate):
        '''
        Creates a new survey, updates just surveys table
        RETURNS created survey's id
        '''
        try:
            sql = "INSERT INTO surveys (surveyname, teacher_id, min_choices, closed, results_saved, survey_description, time_begin, time_end)"\
                " VALUES (:surveyname, :teacher_id, :min_choices, :closed, :saved, :desc, :t_b, :t_e) RETURNING id"
            result = db.session.execute(text(sql), {"surveyname":surveyname, "teacher_id":user_id, "min_choices":min_choices, "closed":False, "saved":False, "desc":description, "t_b":begindate, "t_e":enddate})
            db.session.commit()
            return result.fetchone()[0]
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_survey_description(self, survey_id):
        """
        SQL code for getting the desctiption of a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT survey_description FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id":survey_id})
            return result.fetchone()[0]
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_survey_time_begin(self, survey_id):
        '''
        RETURNS date and time as datetime.datetime(year, month, day, hour, minute)
        '''
        try:
            sql = "SELECT time_begin FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id":survey_id})
            return result.fetchone()[0]
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_survey_time_end(self, survey_id):
        '''
        RETURNS date and time as datetime.datetime(year, month, day, hour, minute)
        '''
        try:
            sql = "SELECT time_end FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id":survey_id})
            return result.fetchone()[0]
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False


    def fetch_all_active_surveys(self, teacher_id):
        '''Returns a list of all surveys in the database'''
        sql = text("SELECT id, surveyname, closed, results_saved, time_end FROM surveys WHERE (teacher_id=:teacher_id AND closed=False)")
        result = db.session.execute(sql, {"teacher_id":teacher_id})
        all_surveys = result.fetchall()
        return all_surveys

    def fetch_survey_responses(self, survey):
        '''Returns a list of answers submitted to a certain survey'''
        sql = text ("SELECT user_id, ranking, rejections, reason FROM user_survey_rankings " +
                    "WHERE survey_id=:survey AND deleted IS FALSE")
        result = db.session.execute(sql, {"survey":survey})
        responses = result.fetchall()
        return responses
    
    def get_list_active_answered(self, user_id):
        """
        SQL code for getting a list of surveys that are active, that have been answered by the user

        args:
            user_id: The id of the user
        """
        try:
            sql = "SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end FROM surveys s, user_survey_rankings r"\
                "  WHERE (r.survey_id=s.id AND r.user_id=:user_id AND s.closed = False AND r.deleted = False)"
            result = db.session.execute(text(sql), {"user_id":user_id})
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def get_list_closed_answered(self, user_id):
        """
        SQL code for getting a list of surveys that are closed, that have been answered by the user

        args:
            user_id: The id of the user
        """
        try:
            sql = "SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end FROM surveys s, user_survey_rankings r"\
                "  WHERE (r.survey_id=s.id AND r.user_id=:user_id AND s.closed = True AND r.deleted = False)"
            result = db.session.execute(text(sql), {"user_id":user_id})
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

survey_repository = SurveyRepository()
