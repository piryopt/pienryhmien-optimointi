from sqlalchemy import text
from src import db

class SurveyRepository:
    def get_survey(self, survey_id):
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
        try:
            sql = "UPDATE surveys SET closed = True WHERE (id=:survey_id and teacher_id=:teacher_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "teacher_id":teacher_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def open_survey(self, survey_id, teacher_id):
        try:
            sql = "UPDATE surveys SET closed = False WHERE (id=:survey_id and teacher_id=:teacher_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "teacher_id":teacher_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_active_surveys(self, teacher_id):
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
        try:
            sql = "SELECT id, surveyname, closed, results_saved FROM surveys WHERE (teacher_id=:teacher_id AND closed=True) ORDER BY id ASC"
            result = db.session.execute(text(sql), {"teacher_id":teacher_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def update_survey_answered(self, survey_id):
        try:
            sql = "UPDATE surveys SET results_saved = True WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id":survey_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    
    def create_new_survey(self, surveyname, user_id, min_choices, description):
        '''
        Creates a new survey, updates just surveys table
        RETURNS created survey's id
        '''

        sql = "INSERT INTO surveys (surveyname, teacher_id, min_choices, closed, results_saved, survey_description)"\
            " VALUES (:surveyname, :teacher_id, :min_choices, :closed, :saved, :desc) RETURNING id"
        result = db.session.execute(text(sql), {"surveyname":surveyname, "teacher_id":user_id, "min_choices":min_choices, "closed":False, "saved":False, "desc":description})
        db.session.commit()
        return result.fetchone()[0]

    
    def get_survey_description(self, survey_id):
        sql = "SELECT survey_description FROM surveys WHERE id=:id"
        result = db.session.execute(text(sql), {"id":survey_id})
        return result.fetchone()[0]

survey_repository = SurveyRepository()
