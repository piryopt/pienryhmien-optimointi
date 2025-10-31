from flask_babel import gettext
from src.repositories.feedback_repository import feedback_repository as default_feedback_repository
from src.services.user_service import user_service as default_user_service


class FeedbackService:
    def __init__(self, feedback_repository=default_feedback_repository, user_service=default_user_service):
        """
        Initalizes the service for feedback with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            feedback_repository: The repository for feedback
            user_service: The service for users

        """
        self._feedback_repository = feedback_repository
        self._user_service = user_service

    def new_feedback(self, user_id, data):
        """
        Create a new feedback entry.

        args:
            user_id: The id of the user submitting the feedback
            data: A dictionary containing the data from the form. Contains the title, type and content
        """
        title = data.get("title", "") or ""
        if len(title) < 3:
            key = "title_too_short"
            msg = gettext("Otsikko on liian lyhyt! Merkkimäärän täytyy olla vähintään 3.")
            return (False, key, msg)
        if len(title) > 50:
            key = "title_too_long"
            msg = gettext("Otsikko on liian pitkä! Merkkimäärä saa olla enintään 50.")
            return (False, key, msg)

        content = data.get("content", "") or ""
        if len(content) < 5:
            key = "content_too_short"
            msg = gettext("Sisältö on liian lyhyt! Merkkimäärän täytyy olla vähintään 5.")
            return (False, key, msg)
        if len(content) > 1500:
            key = "content_too_long"
            msg = gettext("Sisältö on liian pitkä! Merkkimäärä saa olla enintään 1500.")
            return (False, key, msg)

        feedback_type = data.get("type", "palaute")

        check_title = self._feedback_repository.check_unsolved_title_doesnt_exist(user_id, title)
        if not check_title:
            key = "duplicate_title"
            msg = gettext("Olet jo luonut palautteen tällä otsikolla!")
            return (False, key, msg)

        inserted_id = self._feedback_repository.new_feedback(user_id, title, feedback_type, content)
        if not inserted_id:
            key = "server_error"
            msg = gettext("Palautteen antamisessa oli ongelma!")
            return (False, key, msg)
        
        key = "feedback_sent"
        msg = gettext("Palautteen antaminen onnistui")
        return (True, key, msg, inserted_id)

    def get_feedback(self, feedback_id):
        """
        Get data of a feedback

        args:
            feedback_id: The id of the feedback
        """
        return self._feedback_repository.get_feedback(feedback_id)

    def get_unsolved_feedback(self):
        """
        Get a list of all feedback that hasn't been solved.
        """
        return self._feedback_repository.get_feedback_by_solved(False)

    def get_solved_feedback(self):
        """
        Get a list of all feedback that has been solved.
        """
        return self._feedback_repository.get_feedback_by_solved(True)

    def mark_feedback_solved(self, feedback_id):
        """
        Solve a feedback. It wont appear on the feedback page anymore.
        """
        success = self._feedback_repository.mark_feedback_solved(feedback_id)
        return success


feedback_service = FeedbackService()
