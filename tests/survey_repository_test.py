import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User

class TestSurveyRepository(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_check_if_survey_exists(self):
        """
        Create new survey and test if it exists and also test if the surveyname exists
        """
        test_survey1_id = sr.add_new_survey("Test survey 1")
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
        """
        test_survey2_id = sr.add_new_survey("Test survey 2")
        for i in range(3):
            sr.add_new_survey_choice(test_survey2_id, "test" + str(i) + "choice", 10, "info1", "info2")
        n = len(sr.find_survey_choices(test_survey2_id))
        self.assertEqual(n, 3)

    def test_check_that_survey_choice_doesnt_exist(self):
        """
        Test that survey choice with invalid id doesn't exist
        """
        exists = sr.get_survey_choice(-1)
        self.assertEqual(False, exists)

    def test_user_rankings(self):
        """
        Test that adding and deleting user rankings works
        """
        ur.register(User("Testosterone Tester", 1010101011, "testosterone.tester@test.com", True))
        user_id = ur.find_by_email("testosterone.tester@test.com").id
        test_survey3_id = sr.add_new_survey("Test survey 3")
        for i in range(3):
            sr.add_new_survey_choice(test_survey3_id, "test" + str(i) + "choice", 10, "info1", "info2")
        sr.add_user_ranking(user_id, test_survey3_id, "1,2,3")
        ranking = sr.get_user_ranking(user_id, test_survey3_id)
        self.assertEqual(ranking[3], "1,2,3")

        sr.delete_user_ranking(user_id, test_survey3_id)
        ranking = sr.get_user_ranking(user_id, test_survey3_id)

        self.assertEqual(ranking, False)

    def test_survey_name_exists(self):
        """
        Test that surveyname exists
        """
        test_survey4_id = sr.add_new_survey("Test survey 4")
        exists = sr.survey_name_exists("Test survey 4")
        self.assertEqual(True, exists)

    def test_survey_name_doesnt_exist(self):
        """
        Test that surveyname doesn't exist
        """
        test_survey5_name = "Test survey 5"
        exists = sr.survey_name_exists(test_survey5_name)
        self.assertEqual(False, exists)

if __name__ == "__main__":
    unittest.main()
