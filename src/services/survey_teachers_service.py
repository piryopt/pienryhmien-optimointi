from src.repositories.survey_teachers_repository import (
    survey_teachers_repository as default_survey_teachers_repository
)
from src.repositories.user_repository import (
    user_repository as default_user_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class SurveyTeachersService:
    def __init__(self, survey_teachers_repository=default_survey_teachers_repository, user_repository = default_user_repository,
                 survey_repository = default_survey_repository):
        """
        Initalizes the service for survey_teachers with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository
        
        args and variables:
            survey_teachers_repository: The repository for surveys
            user_repository: The repository for users
            survey_repository: The repository for surveys

        """
        self._survey_teachers_repository = survey_teachers_repository
        self._user_repository = user_repository
        self._survey_repository = survey_repository

    def add_teacher_to_survey(self, survey_id, teacher_email):
        """
        Add a teacher to a survey. Only teachers can be added.
        """
        # Verify that a user with the email exists and that the user has teacher privileges
        user = self._user_repository.find_by_email(teacher_email)
        if not user:
            message = f"Sähköpostiosoitetta ei löydetty järjestelmästä! Onko {teacher_email} kirjautunut aikaisemmin Jakajaan?"
            return (False, message)
        
        if not user.isteacher:
            message = "Sähköpostiosoite ei kuulu opettajalle!"
            return (False, message)

        # Check that the survey exists
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            message = "SURVEY DOES NOT EXIST!"
            return (False, message)

        # Check that the user that is being added to the survey doesn't already have access
        teacher_id = user.id
        exists = self._survey_teachers_repository.check_if_teacher_in_survey(survey_id, teacher_id)
        if exists:
            message = "Opettajalla on jo oikeudet kyselyyn!"
            return (False, message)
        
        # Everything checks out, give the teacher access to the survey
        success = self._survey_teachers_repository.add_teacher_to_survey(survey_id, teacher_id)
        if not success:
            message = "ERROR IN ADDING TEACHER TO SURVEY!"
            return (False, message)
        message = f"{teacher_email} sai oikeudet kyselyyn!"
        return (True, message)

survey_teachers_service = SurveyTeachersService()
