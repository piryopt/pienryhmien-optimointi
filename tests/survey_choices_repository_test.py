import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as so
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestSurveyChoicesRepository(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
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
        self.survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
        so.add_owner_to_survey(self.survey_id, self.user_id)
        self.choice_id = scr.create_new_survey_choice(self.survey_id, "choice 1", 10, 5, False)
        self.choice_id2 = scr.create_new_survey_choice(self.survey_id, "choice 2", 10, 5, False)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_find_survey_choices(self):
        """
        Test that the lenght of a list of survey choices for a survey is correct
        """
        choice_list = scr.find_survey_choices(self.survey_id)
        self.assertEqual(2, len(choice_list))

    def test_get_survey_choice(self):
        """
        Test that getting a survey choice works
        """
        choice = scr.get_survey_choice(self.choice_id)
        self.assertEqual(choice.name, "choice 1")

    def test_get_survey_choice_returns_false_forn_nonexistant_choice(self):
        """
        Test that getting a survey choice returns False if choice doesn't exist
        """
        choice = scr.get_survey_choice(self.choice_id+12)
        self.assertEqual(choice, False)

    def test_create_new_survey_choice_returns_false_for_exception(self):
        """
        Test that a survey choice is not added if there's an error in survey id
        and that return is False
        """
        success = scr.create_new_survey_choice("not a survey", "choice 1", 10, 5, False)
        self.assertEqual(success, False)

    def test_get_invalid_choice(self):
        """
        Test that getting an invalid survey choice behaves the correct way
        """
        choice = scr.get_survey_choice("ITSNOTREAL")
        self.assertEqual(choice, False)

    def test_edit_choice_group_size(self):
        """
        Tests that group size is edited and the correct group size saved
        """
        success = scr.edit_choice_group_size(self.survey_id, "choice 1", 5)
        self.assertEqual(success, True)
        new_size = scr.get_survey_choice(self.choice_id)
        self.assertEqual(new_size.max_spaces, 5)

    def test_create_new_choice_info(self):
        """
        Test that create_new_choice_info() works and returns True
        """
        success = scr.create_new_choice_info(self.choice_id, "Priority", "5", False)
        self.assertEqual(success, True)

    def test_create_new_choice_info_not_working_with_false_choice_id(self):
        """
        Test that create_new_choice_info() works and returns True
        """
        success = scr.create_new_choice_info(self.choice_id+56, "Priority", "0", False)
        self.assertEqual(success, False)

    def test_get_choice_additional_infos(self):
        """
        Test that getting the additional info of a survey choice works
        """
        scr.create_new_choice_info(self.choice_id, "Moti", "Vaatio", False)
        info = scr.get_choice_additional_infos(self.choice_id)
        self.assertEqual(info[0].info_key, "Moti")
        self.assertEqual(info[0].info_value, "Vaatio")

    def test_get_all_additional_infos(self):
        """
        Adds additional info on two choices and checks that returned
        number of infos is correct
        """
        scr.create_new_choice_info(self.choice_id, "Priority", "4", False)
        scr.create_new_choice_info(self.choice_id2, "Priority", "11", False)
        info = scr.get_all_additional_infos(self.survey_id)
        self.assertEqual(len(info), 2)

    def test_get_all_additional_infos_not_hidden(self):
        """
        Adds additional info on two choices and checks that returned
        number of infos is correct
        """
        scr.create_new_choice_info(self.choice_id, "Osoite", "Kakkakuja 4", False)
        scr.create_new_choice_info(self.choice_id, "Kaupunki", "Helsinki", True)
        info = scr.get_choice_additional_infos_not_hidden(self.choice_id)

        self.assertEqual(len(info), 1)
        self.assertEqual(info[0][0], "Osoite")
        self.assertEqual(info[0][1], "Kakkakuja 4")

    def test_exceptions(self):
        """
        Test that exceptions return False
        """
        success = scr.find_survey_choices(-1)
        self.assertFalse(success)
        success = scr.get_all_additional_infos(-1)
        self.assertFalse(success)
