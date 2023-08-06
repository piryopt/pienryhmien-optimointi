from sqlalchemy import text
from src import db

class SurveyTeachersRepository:
    def add_teacher_to_survey(self, survey_id, teacher_id):
        """
        SQL code for adding a teacher to a survey.

        args:
            survey_id: The id of the survey
            teacher_id: The id of the teacher
        """
        try:
            sql = "INSERT INTO survey_teachers (survey_id, teacher_id) VALUES (:survey_id, :teacher_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "teacher_id":teacher_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def check_if_teacher_in_survey(self, survey_id, teacher_id):
        """
        SQL code for checking if a teacher already has access to the survey.

        args:
            survey_id: The id of the survey
            teacher_id: The id of the teacher
        """
        try:
            sql = "SELECT * FROM survey_teachers WHERE survey_id=:survey_id AND teacher_id=:teacher_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "teacher_id":teacher_id})
            teacher = result.fetchone()
            if not teacher:
                return False
            return teacher
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
survey_teachers_repository = SurveyTeachersRepository()
