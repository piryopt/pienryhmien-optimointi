import unittest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.services.survey_owners_service import survey_owners_service as sos
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime
import json


class TestSurveyOwnersService(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
        self.app.config["BABEL_DEFAULT_LOCALE"] = "fi"

        babel = Babel(self.app)
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        clear_database()

        user = User("Not on tren Testerr", "tren4lyfe@tester.com", True)
        user2 = User("Hashtag natty", "anabolics4lyfe@tester.com", False)
        ur.register(user)
        ur.register(user2)
        self.user_id = ur.find_by_email(user.email)[0]
        self.user_email = user.email
        self.user_email_student = user2.email

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_add_owner_to_survey(self):
        """
        Test that adding a owner to a survey works and check that it cannot be added again
        """
        with open("tests/test_files/test_survey1.json", "r") as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(
            json_object["choices"], "Test survey 1", self.user_id, json_object["surveyInformation"], 1, "01.01.2024", "02:02"
        )
        (success, message) = sos.add_owner_to_survey(survey_id, self.user_email)
        self.assertEqual(success, True)
        (success, message) = sos.add_owner_to_survey(survey_id, self.user_email)
        self.assertEqual(success, False)

    def test_add_owner_to_survey_invalid_email(self):
        """
        Test that adding an email that isn't in the database works correctly
        """
        with open("tests/test_files/test_survey1.json", "r") as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(
            json_object["choices"], "Test survey 2", self.user_id, json_object["surveyInformation"], 1, "01.01.2024", "02:02"
        )
        (success, message) = sos.add_owner_to_survey(survey_id, "trt@tester.com")
        self.assertEqual(success, False)

    def test_add_owner_to_invalid_survey(self):
        """
        Test that you cannot add a owner to an invalid survey
        """
        with open("tests/test_files/test_survey1.json", "r") as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        (success, message) = sos.add_owner_to_survey("ITSNOTREAL", self.user_email)
        self.assertEqual(success, False)
