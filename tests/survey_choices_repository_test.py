import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestSurveyChoicesRepository(unittest.TestCase):
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
        user1 = User("Not on tren Testerr", 101010101, "feelsbadman@tester.com", True)
        user2 = User("Not on anabolic", 101010101, "anabolic@tester.com", True)
        self.ur.register(user1)
        self.ur.register(user2)
        self.user_id = ur.find_by_email(user1.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_find_survey_choices(self):
        survey_id = sr.create_new_survey("Test survey 1", self.user_id, 10, "Motivaatio")
        scr.create_new_survey_choice(survey_id, "choice 1", 10)
        scr.create_new_survey_choice(survey_id, "choice 2", 10)
        choice_list = scr.find_survey_choices(survey_id)
        self.assertEqual(2, len(choice_list))

    def test_get_choice(self):
        survey_id = sr.create_new_survey("Test survey 2", self.user_id, 10, "Motivaatio")
        choice_id = scr.create_new_survey_choice(survey_id, "choice 1", 10)
        choice = scr.get_survey_choice(choice_id)
        self.assertEqual(choice.name, "choice 1")

    def test_get_invalid_choice(self):
        choice = scr.get_survey_choice(-1)
        self.assertEqual(choice, False)

    def test_get_choice_info(self):
        survey_id = sr.create_new_survey("Test survey 3", self.user_id, 10, "Motivaatio")
        choice_id = scr.create_new_survey_choice(survey_id, "choice 1", 10)
        scr.create_new_choice_info(choice_id, "Moti", "Vaatio")
        info = scr.get_choice_additional_infos(choice_id)
        self.assertEqual(info[0].info_key, "Moti")
        self.assertEqual(info[0].info_value, "Vaatio")

    def test_get_choice_name(self):
        survey_id = sr.create_new_survey("Test survey 4", self.user_id, 10, "Motivaatio")
        choice_id = scr.create_new_survey_choice(survey_id, "moti 1", 10)
        name_and_spaces = scr.get_choice_name_and_spaces(choice_id)
        self.assertEqual(name_and_spaces.name, "moti 1")