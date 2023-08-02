import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime

class TestSurveyRepository(unittest.TestCase):
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

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_get_survey(self):
        """
        Create new survey and test if it exists and also test if the surveyname exists
        """
        test_survey1_id = sr.create_new_survey("Test survey 1", self.user_id, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        survey = sr.get_survey(test_survey1_id)
        self.assertEqual(survey[0], test_survey1_id)

    def test_check_that_survey_doesnt_exist(self):
        """
        Test that survey with invalid id doesn't exist
        """
        exists = sr.get_survey(-1)
        self.assertEqual(False, exists)

    def test_survey_name_doesnt_exist(self):
        """
        Test that surveyname doesn't exist
        """
        test_survey5_name = "Test survey 2"
        exists = sr.survey_name_exists(test_survey5_name, self.user_id)
        self.assertEqual(False, exists)

    def test_count_created_surveys(self):
        """
        Test that the number of created surveys is correct
        """

        sr.create_new_survey("Test survey 3", self.user_id2, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        sr.create_new_survey("Test survey 4", self.user_id2, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        count = sr.count_created_surveys(self.user_id2)
        self.assertEqual(2, count)

    def test_close_survey(self):
        """
        Test that closing a survey works
        """
        survey_id = sr.create_new_survey("Test survey 5", self.user_id2, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        sr.close_survey(survey_id, self.user_id2)

        closed = sr.get_survey(survey_id).closed
        self.assertEqual(True, closed)

    def test_get_active_surveys(self):
        """
        Test that getting a list of active surveys works
        """
        sr.create_new_survey("Test survey 6", self.user_id2, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        active_list = sr.get_active_surveys(self.user_id2)
        self.assertEqual(1, len(active_list))

    def test_get_closed_surveys(self):
        """
        Test that getting a list of closed surveys works
        """
        survey_id = sr.create_new_survey("Test survey 7", self.user_id2, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        sr.close_survey(survey_id, self.user_id2)
        closed_list = sr.get_closed_surveys(self.user_id2)
        self.assertEqual(1, len(closed_list))

    def test_open_survey(self):
        """
        Test that closing a survey works
        """
        survey_id = sr.create_new_survey("Test survey 8", self.user_id, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        sr.close_survey(survey_id, self.user_id)

        closed = sr.get_survey(survey_id).closed
        self.assertEqual(True, closed)

        sr.open_survey(survey_id, self.user_id)
        opened = sr.get_survey(survey_id).closed
        self.assertEqual(False, opened)

    def test_survey_name_exists(self):
        """
        Test that a survey name exists when a survey is added to the database
        """
        sr.create_new_survey("Test survey 9", self.user_id, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        exists = sr.survey_name_exists("Test survey 9", self.user_id)
        self.assertEqual(True, exists)

    def test_count_created_surveys_invalid_id(self):
        """
        Test that the function behaves correctly when trying to get the list of all created surveys for an invalid user
        """
        exists = sr.count_created_surveys(-1)
        self.assertEqual(False, exists)

    def test_count_active_surveys_invalid_id(self):
        """
        Test that the function behaves correctly when trying to get the list of active created surveys for an invalid user
        """
        exists = sr.get_active_surveys(-1)
        self.assertEqual(False, exists)

    def test_survey_description(self):
        """
        Test that getting the description of a survey works
        """
        survey_id = sr.create_new_survey("Test survey 10", self.user_id, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        desc = sr.get_survey_description(survey_id)
        self.assertEqual("Motivaatio", desc)

    def test_survey_answered(self):
        """
        Test that updating a survey so that it has its results saved works
        """
        survey_id = sr.create_new_survey("Test survey 11", self.user_id, 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        sr.update_survey_answered(survey_id)
        answered = sr.get_survey(survey_id).results_saved
        self.assertEqual(True, answered)

    def test_survey_time_begin_correct(self):
        """
        Test that the begin time of a created survey is correct
        """
        survey_id = sr.create_new_survey("Test survey 666", self.user_id, 10, "Ei motivaatiota", "2023-01-01 02:03", "2024-01-01 02:02")
        time = sr.get_survey_time_begin(survey_id)

        self.assertEqual(time, datetime.datetime(2023, 1, 1, 2, 3))

    def test_survey_time_end_correct(self):
        """
        Test that the ending time of a created survey is correct
        """
        survey_id = sr.create_new_survey("Test survey 666", self.user_id, 10, "Ei motivaatiota", "2023-10-02 13:01", "2024-06-19 12:01")
        time = sr.get_survey_time_end(survey_id)

        self.assertEqual(time, datetime.datetime(2024, 6, 19, 12, 1))
