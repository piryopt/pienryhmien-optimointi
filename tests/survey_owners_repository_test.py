import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as sor
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestSurveyOwnersRepository(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        clear_database()

        self.ur = ur
        user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
        user2 = User("Not on anabolic", "anabolic@tester.com", True)
        user3 = User("trt enjoyer", "ttrt@tester.com", True)
        self.ur.register(user1)
        self.ur.register(user2)
        self.ur.register(user3)
        self.user_id = ur.find_by_email(user1.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]
        self.user_id3 = ur.find_by_email(user3.email)[0]

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_add_owner_to_survey(self):
        """
        Test that adding an owner to a survey works. Also test if owner added to survey
        """
        survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
        success_add = sor.add_owner_to_survey(survey_id, self.user_id)
        self.assertEqual(success_add, True)
        owner = sor.check_if_owner_in_survey(survey_id, self.user_id)
        self.assertEqual(owner.survey_id, survey_id)

    def test_add_owner_invalid_survey(self):
        """
        Test that you cannot add a owner to an invalid survey
        """
        success_add = sor.add_owner_to_survey("ITSNOTREAL", self.user_id)
        self.assertEqual(success_add, False)

    def test_add_owner_invalid_survey(self):
        """
        Test that you cannot get an invalid owner from an invalid survey
        """
        success_get = sor.check_if_owner_in_survey("ITSNOTREAL", -1)
        self.assertEqual(success_get, False)

    def test_exceptions(self):
        """
        Test that exceptions return False
        """
        success = sor.add_owner_to_survey(-1, self.user_id)
        self.assertFalse(success)
        success = sor.check_if_owner_in_survey(-1, self.user_id)
        self.assertFalse(success)
