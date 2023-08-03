from flask import session # pylint: disable=R0401
from src.entities.user import User
from src.repositories.user_repository import (
    user_repository as default_user_repository
)

class UserService:
    def __init__(self, user_repositroy=default_user_repository):
        """
        Initalized the service for users with the repositories needed. The purpose of this class is to handle what happens after the SQL code in the
        corresponding repository

        args and variables:
            user_repositroy: The repository for users
        """
        self._user_repository = user_repositroy

    def check_credentials(self, email):
        """
        Check that the email is registered. If it is, log that user in and update session variables.
        Delete before production!

        args:
            email: The email address of the user trying to log in
        """
        if not email:
            return False
        user = self._user_repository.find_by_email(email)
        if not user:
            return False
        session["email"] = user.email
        session["user_id"] = user.id
        session["full_name"] = user.name
        if user.isteacher:
            session["role"] = "Opettaja"
        else:
            session["role"] = "Opiskelija"
        return True

    def create_user(self, name, student_number, email, isteacher):
        """
        Creates a user with the provided data. Delete before production!

        args:
            name: The name of the user
            student_number: the student number of the user
            email: The email address of the user
            isteacher: True/False depending on if the user is a teacher/student
        """
        if not self.validate(name, student_number):
            return False
        new_user = User(name, student_number, email, isteacher)
        user = self._user_repository.register(new_user)
        return user

    def validate(self, name, student_number):
        """
        Validate that name and student number are correct. They cannot be empty values

        args:
            name: The name of the user
            student_number: the student number of the user
        """
        if not name or not student_number:
            return False
        if len(name) < 1:
            return False
        return True

    def get_student_number(self, user_id):
        """
        Get the student number of a user

        args:
            user_id: The id of the user
        """
        if not id:
            return False
        user = self._user_repository.get_user_data(user_id)
        if not user:
            return False
        student_number = user.student_number
        return student_number

    def get_email(self, user_id):
        """
        Get the email of a user

        args:
            user_id: The id of the user
        """
        if not id:
            return False
        user = self._user_repository.get_user_data(user_id)
        if not user:
            return False
        email = user.email
        return email

    def get_name(self, user_id):
        """
        Get the name of a user

        args:
            user_id: The id of the user
        """
        if not id:
            return False
        user = self._user_repository.get_user_data(user_id)
        if not user:
            return False
        name = user.name
        return name

    def logout(self):
        """
        Logout user from the app. Deletes session data of the user
        """
        del session["email"]
        del session["user_id"]
        del session["full_name"]
        del session["role"]

    def find_by_email(self, email):
        """
        Find user by email address

        args:
            email: The email of the user
        """
        return self._user_repository.find_by_email(email)
    
    def make_user_teacher(self, email): # don't remove, needed later
        """
        Give a user teacher privileges

        args:
            email: The email of the user
        """
        self._user_repository.make_user_teacher(email)

    def check_if_teacher(self, user_id):
        """
        Check if the user has teacher privileges

        args:
            user_id: The id of the user
        """
        user = self._user_repository.get_user_data(user_id)
        return user.isteacher

user_service = UserService()
