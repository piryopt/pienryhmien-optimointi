from sqlalchemy import text
from src import db

class FinalGroupRepository:
    def save_result(self, user_id, survey_id, choice_id):
        try:
            sql = "INSERT INTO final_group (user_id, survey_id, choice_id) VALUES (:user_id, :survey_id, :choice_id)"
            db.session.execute(text(sql), {"user_id":user_id, "survey_id":survey_id, "choice_id":choice_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

final_group_repository = FinalGroupRepository()
