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
            sql = "INSERT INTO feedback (user_id, title, type, content, solved) VALUES (:user_id, :title, :type, :content, :solved)"
            parameters = {
                "user_id": user_id if user_id != 0 else None,
                "title": title,
                "type": type,
                "content": content,
                "solved": False,
            }
            db.session.execute(text(sql), parameters)
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_feedback(self, feedback_id):
        """
        SQL code for getting content of feedback

        args:
            feedback_id: The id of the feedback
        """
        try:
            sql = """
                SELECT F.id, F.title, F.type, U.email, F.content, F.solved
                FROM feedback F LEFT JOIN users U ON F.user_id = U.id 
                WHERE F.id = :feedback_id
            """
            result = db.session.execute(text(sql), {"feedback_id": feedback_id})
            feedback = result.fetchone()
            return feedback
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def get_feedback_by_solved(self, solved):
        """
        SQL code for getting a list of feedback which haven't been solved
        """
        try:
            sql = """
                SELECT F.id, F.title, F.type, U.email
                FROM feedback F LEFT JOIN users U 
                ON F.user_id = U.id
                WHERE F.solved = :solved
            """
            result = db.session.execute(text(sql), {"solved": solved})
            feedback = result.fetchall()
            return feedback
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def check_unsolved_title_doesnt_exist(self, user_id, title):
        """
        SQL code for checking if the user has submitted a same named feedback. This should reduce spam.
        """
        try:
            sql = "SELECT * FROM feedback WHERE user_id=:user_id AND title=:title"
            result = db.session.execute(text(sql), {"user_id": user_id, "title": title})
            feedback = result.fetchall()
            if not feedback:
                return True
            return False
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def mark_feedback_solved(self, feedback_id):
        """
        SQL code for closing a feedback
        """
        try:
            sql = "UPDATE feedback SET solved=True WHERE id=:feedback_id"
            db.session.execute(text(sql), {"feedback_id": feedback_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False


feedback_repository = FeedbackRepository()
