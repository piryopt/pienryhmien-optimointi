from flask import session
from entities.user import User
from repositories.user_repository import (
    user_repository as default_user_repository
)

class UserService:
    def __init__(self, user_repositroy=default_user_repository):
        self._user_repository = user_repositroy

    def check_credentials(self, email, password):
        if not email or not password:
            print("Email and password are required!")
            return False
        user = self._user_repository.find_by_email(email, password)
        if not user:
            print("Invalid username or password")
            return False
        session["email"] = user.email
        session["user_id"] = user.id
        return True

    def create_user(self, firstname, lastname, student_number, email, password1, password2, isteacher):
        if not self.validate(firstname, lastname, student_number, password1, password2):
            return False
        new_user = User(firstname, lastname, student_number, email, password1, isteacher)
        user = self._user_repository.register(new_user)
        return user

    def validate(self, firstname, lastname, student_number, password1, password2):
        if not firstname or not lastname or not student_number or not password1 or not password2:
            print("All fields are required!")
            return False
        if password1 != password2:
            print("Passwords do not match!")
            return False
        if len(firstname) < 2 or len(lastname) < 2:
            print("Name is too short!")
            return False
        if len(password1)  < 4:
            print("Password is too short!")
            return False
        return True

    def logout(self):
        del session["email"]
        del session["user_id"]

user_service = UserService()
