import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_teachers_repository import survey_teachers_repository as st
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
        user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
        user2 = User("Not on anabolic", "anabolic@tester.com", True)
        self.ur.register(user1)
        self.ur.register(user2)
        self.user_id = ur.find_by_email(user1.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]
        self.survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(self.survey_id, self.user_id)
        self.choice_id = scr.create_new_survey_choice(self.survey_id, "choice 1", 10)
        scr.create_new_survey_choice(self.survey_id, "choice 2", 10)

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_find_survey_choices(self):
        """
        Test that the list of survey choices for a survey is correct
        """
        choice_list = scr.find_survey_choices(self.survey_id)
        self.assertEqual(2, len(choice_list))

    def test_get_choice(self):
        """
        Test that getting a survey choice works
        """
        choice = scr.get_survey_choice(self.choice_id)
        self.assertEqual(choice.name, "choice 1")

    def test_get_invalid_choice(self):
        """
        Test that getting an invalid survey choice behaves the correct way
        """
        choice = scr.get_survey_choice("ITSNOTREAL")
        self.assertEqual(choice, False)

    def test_get_choice_info(self):
        """
        Test that getting the info of a survey choice works
        """
        scr.create_new_choice_info(self.choice_id, "Moti", "Vaatio")
        info = scr.get_choice_additional_infos(self.choice_id)
        self.assertEqual(info[0].info_key, "Moti")
        self.assertEqual(info[0].info_value, "Vaatio")
