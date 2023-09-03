from sqlalchemy import text
from src import db

class FeedbackRepository:
    def new_feedback(self, user_id, title, type, content):
        """
        SQL code for creating feedback

        args:
            user_id: The id of the user giving the feedback
            title: The title of the feedback
            type: The type of the feedback: Palaute, bugi, muu
            content: The content of the feedback
        """
        try:
            sql = "INSERT INTO feedback (user_id, title, type, content, solved) VALUES (:user_id, :title, :type, :content, False)"
            db.session.execute(text(sql), {"user_id":user_id, "title":title, "type":type, "content":content})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def get_feedback(self, feedback_id):
        """
        SQL code for getting content of feedback

        args:
            feedback_id: The id of the feedback
        """
        try:
            sql = "SELECT * FROM feedback WHERE id=:feedback_id"
            result = db.session.execute(text(sql), {"feedback_id":feedback_id})
            feedback = result.fetchone()
            if not feedback:
                return False
            return feedback
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def get_unsolved_feedback(self):
        """
        SQL code for getting a list of feedback which haven't been solved
        """
        try:
            sql = "SELECT * FROM feedback WHERE solved=False"
            result = db.session.execute(text(sql))
            feedback = result.fetchall()
            if not feedback:
                return False
            return feedback
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def get_solved_feedback(self):
        """
        SQL code for getting a list of feedback which have been solved
        """
        try:
            sql = "SELECT * FROM feedback WHERE solved=True"
            result = db.session.execute(text(sql))
            feedback = result.fetchall()
            if not feedback:
                return False
            return feedback
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def check_unsolved_title_doesnt_exist(self, user_id, title):
        """
        SQL code for checking if the user has submitted a same named feedback. This should reduce spam.
        """
        try:
            sql = "SELECT * FROM feedback WHERE user_id=:user_id AND title=:title"
            result = db.session.execute(text(sql), {"user_id":user_id, "title":title})
            feedback = result.fetchall()
            if not feedback:
                return True
            return False
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def mark_feedback_solved(self, feedback_id):
        """
        SQL code for closing a feedback
        """
        try:
            sql = "UPDATE feedback SET solved=True WHERE id=:feedback_id"
            db.session.execute(text(sql), {"feedback_id":feedback_id})
            db.session.commit()
            return True
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

feedback_repository = FeedbackRepository()
