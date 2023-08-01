from flask import session # pylint: disable=R0401
from src.entities.user import User
from src.repositories.user_repository import (
    user_repository as default_user_repository
)

class UserService:
    def __init__(self, user_repositroy=default_user_repository):
        self._user_repository = user_repositroy

    def check_credentials(self, email):
        if not email:
            print("Email is required!")
            return False
        user = self._user_repository.find_by_email(email)
        if not user:
            print("Invalid email!")
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
        if not self.validate(name, student_number):
            return False
        new_user = User(name, student_number, email, isteacher)
        user = self._user_repository.register(new_user)
        return user

    def validate(self, name, student_number):
        if not name or not student_number:
            print("All fields are required!")
            return False
        if len(name) < 1:
            print("Name is too short!")
            return False
        return True

    def get_student_number(self, user_id):
        if not id:
            print("user_id required!")
            return False
        user = self._user_repository.get_user_data(user_id)
        if not user:
            return False
        student_number = user.student_number
        return student_number

    def get_email(self, user_id):
        if not id:
            print("user_id required!")
            return False
        user = self._user_repository.get_user_data(user_id)
        if not user:
            return False
        email = user.email
        return email

    def get_name(self, user_id):
        if not id:
            print("user_id required!")
            return False
        user = self._user_repository.get_user_data(user_id)
        if not user:
            return False
        name = user.name
        return name

    def logout(self):
        del session["email"]
        del session["user_id"]
        del session["full_name"]
        del session["role"]

    def find_by_email(self, email):
        return self._user_repository.find_by_email(email)
    
    def make_user_teacher(self, email): # don't remove, needed later
        self._user_repository.make_user_teacher(email)

user_service = UserService()
