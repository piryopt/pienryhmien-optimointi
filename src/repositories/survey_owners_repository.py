from sqlalchemy import text
from src import db

class SurveyOwnersRepository:
    def add_owner_to_survey(self, survey_id, user_id):
        """
        SQL code for adding an owner to a survey.

        args:
            survey_id: The id of the survey
            user_id: The id of the user creating the survey or being added as an owner
        """
        try:
            sql = "INSERT INTO survey_owners (survey_id, user_id) VALUES (:survey_id, :user_id)"
            db.session.execute(text(sql), {"survey_id":survey_id, "user_id":user_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def check_if_owner_in_survey(self, survey_id, user_id):
        """
        SQL code for checking if a user already has access to the survey.

        args:
            survey_id: The id of the survey
            user_id: The id of the user
        """
        try:
            sql = "SELECT * FROM survey_owners WHERE survey_id=:survey_id AND user_id=:user_id"
            result = db.session.execute(text(sql), {"survey_id":survey_id, "user_id":user_id})
            owner = result.fetchone()
            if not owner:
                return False
            return owner
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
survey_owners_repository = SurveyOwnersRepository()
