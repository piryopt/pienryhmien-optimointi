from flask_babel import gettext
from src.repositories.feedback_repository import (
    feedback_repository as default_feedback_repository
)
from src.services.user_service import (
    user_service as default_user_service
)

class FeedbackService:
    def __init__(self, feedback_repository = default_feedback_repository, user_service = default_user_service):
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
        title = data["title"]
        if len(title) < 3:
            message = gettext('Otsikko on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 3.')
            return (False, message)
        if len(title) > 50:
            message = gettext('Otsikko on liian pitkä! Merkkimäärän täytyy olla pienempi kuin 50.')
            return (False, message)

        content = data["content"]
        if len(content) < 5:
            message = gettext('Sisältö on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 5.')
            return (False, message)
        if len(content) > 1500:
            message = gettext('Sisältö on liian pitkä! Merkkimäärän täytyy olla pienempi kuin 1500. Merkkejä oli ')
            return (False, message + len(content))
        
        feedback_type = data["type"]

        check_title = self._feedback_repository.check_unsolved_title_doesnt_exist(user_id, title)
        if not check_title:
            message = gettext('Olet jo luonut palautteen tällä otsikolla!')
            return (False, message)

        success = self._feedback_repository.new_feedback(user_id, title, feedback_type, content)
        if not success:
            message = gettext('Palautteen antamisessa oli ongelma!')
            return (False, message)
        message = gettext('Palautteen antaminen onnistui')
        return (True, message)
    
    def get_feedback(self, feedback_id):
        """
        Get data of a feedback

        args:
            feedback_id: The id of the feedback
        """
        feedback = self._feedback_repository.get_feedback(feedback_id)
        if not feedback:
            return False
        user_id = feedback.user_id
        email = self._user_service.get_email(user_id)
        feedback_list = [feedback.id, feedback.title, feedback.type, email, feedback.content]
        return feedback_list
    
    def get_unsolved_feedback(self):
        """
        Get a list of all feedback that hasn't been solved.
        """
        feedback = self._feedback_repository.get_unsolved_feedback()
        if not feedback:
            return []
        feedback_list = []
        for f in feedback:
            user_id = f.user_id
            email = self._user_service.get_email(user_id)
            feedback_list.append([f.id, f.title, f.type, email])
        return feedback_list
    
    def get_solved_feedback(self):
        """
        Get a list of all feedback that has been solved.
        """
        feedback = self._feedback_repository.get_solved_feedback()
        if not feedback:
            return []
        feedback_list = []
        for f in feedback:
            user_id = f.user_id
            email = self._user_service.get_email(user_id)
            feedback_list.append([f.id, f.title, f.type, email])
        return feedback_list
    
    def mark_feedback_solved(self, feedback_id):
        """
        Solve a feedback. It wont appear on the feedback page anymore.
        """
        success = self._feedback_repository.mark_feedback_solved(feedback_id)
        return success




feedback_service = FeedbackService()
