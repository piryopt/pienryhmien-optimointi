import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.parsers import clear_database

class TestSurveyRepository(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

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

    def test_not_clear_db_begin_rep(self):
        clear_database()

    def test_check_if_survey_exists(self):
        """
        Create new survey and test if it exists and also test if the surveyname exists
        """
        test_survey1_id = sr.add_new_survey("Test survey 1", self.user_id)
        survey = sr.check_if_survey_exists(test_survey1_id)
        self.assertEqual(survey[0], test_survey1_id)

    def test_check_that_survey_doesnt_exist(self):
        """
        Test that survey with invalid id doesn't exist
        """
        exists = sr.check_if_survey_exists(-1)
        self.assertEqual(False, exists)

    def test_find_survey_choices(self):
        """
        Test that adding and finding survey choices works
        
        test_survey2_id = sr.add_new_survey("Test survey 2", self.user_id)
        for i in range(3):
            sr.add_new_survey_choice(test_survey2_id, "test" + str(i) + "choice", 10, "info1", "info2")
        n = len(sr.find_survey_choices(test_survey2_id))
        self.assertEqual(n, 3)
        """

    def test_check_that_survey_choice_doesnt_exist(self):
        """
        Test that survey choice with invalid id doesn't exist
        """
        exists = sr.get_survey_choice(-1)
        self.assertEqual(False, exists)

    def test_user_rankings(self):
        """
        Test that adding and deleting user rankings works
        
        test_survey3_id = sr.add_new_survey("Test survey 3", self.user_id)
        for i in range(3):
            sr.add_new_survey_choice(test_survey3_id, "test" + str(i) + "choice", 10, "info1", "info2")
        sr.add_user_ranking(self.user_id, test_survey3_id, "1,2,3")
        ranking = sr.get_user_ranking(self.user_id, test_survey3_id)
        self.assertEqual(ranking[3], "1,2,3")

        sr.delete_user_ranking(self.user_id, test_survey3_id)
        ranking = sr.get_user_ranking(self.user_id, test_survey3_id)

        self.assertEqual(ranking, False)
        """

    def test_survey_name_exists(self):
        """
        Test that surveyname exists
        """
        sr.add_new_survey("Test survey 4", self.user_id)
        exists = sr.survey_name_exists("Test survey 4", self.user_id)
        self.assertEqual(True, exists)

    def test_survey_name_doesnt_exist(self):
        """
        Test that surveyname doesn't exist
        """
        test_survey5_name = "Test survey 5"
        exists = sr.survey_name_exists(test_survey5_name, self.user_id)
        self.assertEqual(False, exists)

    def test_count_created_surveys(self):
        """
        Test that the number of created surveys is correct
        """

        sr.add_new_survey("Test survey 5", self.user_id2)
        sr.add_new_survey("Test survey 6", self.user_id2)
        count = sr.count_created_surveys(self.user_id2)
        self.assertEqual(2, count)

    def test_close_survey(self):
        """
        Test that closing a survey works
        """
        survey_id = sr.add_new_survey("Test survey 7", self.user_id)
        sr.close_survey(survey_id, self.user_id)

        closed = sr.check_if_survey_exists(survey_id).closed
        self.assertEqual(True, closed)

    def test_get_active_surveys(self):
        """
        Test that getting a list of active surveys works
        """
        active_list = sr.get_active_surveys(self.user_id2)
        self.assertEqual(2, len(active_list))

    def test_get_closed_surveys(self):
        """
        Test that getting a list of closed surveys works
        """
        survey_id = sr.add_new_survey("Test survey 8", self.user_id2)
        sr.close_survey(survey_id, self.user_id2)
        closed_list = sr.get_closed_surveys(self.user_id2)
        self.assertEqual(1, len(closed_list))

    def test_open_survey(self):
        """
        Test that closing a survey works
        """
        survey_id = sr.add_new_survey("Test survey 8", self.user_id)
        sr.close_survey(survey_id, self.user_id)

        closed = sr.check_if_survey_exists(survey_id).closed
        self.assertEqual(True, closed)

        sr.open_survey(survey_id, self.user_id)
        opened = sr.check_if_survey_exists(survey_id).closed
        self.assertEqual(False, opened)

    
    def test_not_clear_db_end_rep(self):
        clear_database()


if __name__ == "__main__":
    unittest.main()
