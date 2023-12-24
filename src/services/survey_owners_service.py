from src.repositories.survey_owners_repository import (
    survey_owners_repository as default_survey_owners_repository
)
from src.repositories.user_repository import (
    user_repository as default_user_repository
)
from src.repositories.survey_repository import (
    survey_repository as default_survey_repository
)

class SurveyOwnersService:
    def __init__(self, survey_owners_repository=default_survey_owners_repository, user_repository = default_user_repository,
                 survey_repository = default_survey_repository):
        """
        Initalizes the service for survey_owners with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository
        
        args and variables:
            survey_owners_repository: The repository for survey owners
            user_repository: The repository for users
            survey_repository: The repository for surveys

        """
        self._survey_owners_repository = survey_owners_repository
        self._user_repository = user_repository
        self._survey_repository = survey_repository

    def add_owner_to_survey(self, survey_id, user_email):
        """
        Add a user to a survey as an owner.
        """
        # Verify that a user with the email exists
        user = self._user_repository.find_by_email(user_email)
        if not user:
            message = f"Sähköpostiosoitetta ei löydetty järjestelmästä! Onko {user_email} kirjautunut aikaisemmin Jakajaan?"
            return (False, message)
        
        # Check that the survey exists
        survey = self._survey_repository.get_survey(survey_id)
        if not survey:
            message = "SURVEY DOES NOT EXIST!"
            return (False, message)

        # Check that the user that is being added to the survey doesn't already have access
        user_id = user.id
        exists = self._survey_owners_repository.check_if_owner_in_survey(survey_id, user_id)
        if exists:
            message = "Opettajalla on jo oikeudet kyselyyn!"
            return (False, message)
        
        # Everything checks out, give the user access to the survey
        success = self._survey_owners_repository.add_owner_to_survey(survey_id, user_id)
        if not success:
            message = "ERROR IN ADDING USER TO SURVEY!"
            return (False, message)
        message = f"{user_email} sai oikeudet kyselyyn!"
        return (True, message)
    
    def check_if_user_is_survey_owner(self, survey_id, user_id):
        """
        Checks if the user has access to the survey as an owner
        """
        owner = self._survey_owners_repository.check_if_owner_in_survey(survey_id, user_id)
        return owner

survey_owners_service = SurveyOwnersService()
