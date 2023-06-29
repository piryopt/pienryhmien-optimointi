import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.services.survey_service import survey_service as ss
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.services.user_service import user_service as us
from src.entities.user import User

class TestSurveyService(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        user = User("Not on tren Testerr", 101010101, "tren4lyfe@tester.com", True)
        ur.register(user)
        self.user_id = ur.find_by_email(user.email)[0]


    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_invalid_survey_id_list_choices(self):
        """
        Test that no list of choices is returned for an invalid survey id
        """
        exists = ss.get_list_of_survey_choices(-1)
        self.assertEqual(False, exists)

    def test_survey_choice_list(self):
        """
        Test that a list of survey choices is returned for a valid survey id
        """
        test_survey1_id = sr.add_new_survey("Survey service test 1")
        for i in range(3):
            sr.add_new_survey_choice(test_survey1_id, "test" + str(i) + "choice", 10, "info1", "info2")
        choice_list = ss.get_list_of_survey_choices(test_survey1_id)
        self.assertEqual(3, len(choice_list))

    def test_get_survey_name(self):
        """
        Test that a survey name is returned with a valid survey id
        """
        test_survey2_id = sr.add_new_survey("Survey service test 2")
        name = ss.get_survey_name(test_survey2_id)
        self.assertEqual(name, "Survey service test 2")

    def test_get_survey_name_nonexisting_id(self):
        """
        Test that no survey name is returned for an invalid survey id
        """
        name = ss.get_survey_name(-1)
        self.assertEqual(name, False)

    def test_user_ranking_doesnt_exist_and_cant_delete(self):
        test_survey3_id = sr.add_new_survey("Survey service test 3")
        exists = ss.user_ranking_exists(test_survey3_id, self.user_id)
        self.assertEqual(exists, False)
        deleted = ss.delete_ranking(test_survey3_id, self.user_id)
        self.assertEqual(False, deleted)


    def test_add_user_ranking_and_delete_it(self):
        test_survey4_id = sr.add_new_survey("Survey service test 4")
        for i in range(3):
            sr.add_new_survey_choice(test_survey4_id, "test" + str(i) + "choice", 10, "info1", "info2")
        exists = ss.add_user_ranking(test_survey4_id, "1,2,3,4", self.user_id)
        self.assertEqual(True, exists)
        deleted = ss.delete_ranking(test_survey4_id, self.user_id)
        self.assertEqual(True, deleted)

    def test_user_ranking_exists(self):
        test_survey5_id = sr.add_new_survey("Survey service test 5")
        for i in range(3):
            sr.add_new_survey_choice(test_survey5_id, "test" + str(i) + "choice", 10, "info1", "info2")
        ss.add_user_ranking(test_survey5_id, "1,2,3,4", self.user_id)
        ranking = ss.user_ranking_exists(test_survey5_id, self.user_id)
        self.assertEqual("1,2,3,4", ranking[3])

    def test_add_new_survey(self):
        name = "Survey service test 6 new survey"
        ss.add_new_survey(name)
        exists = ss.add_new_survey(name)
        self.assertEqual(False, exists)

    def test_short_name_new_survey(self):
        name = "asd"
        exists = ss.add_new_survey(name)
        self.assertEqual(False, exists)

    def test_add_invalid_survey_choice(self):
        name = "Testien kirjoittaminen on 6/5"
        exists = ss.add_survey_choice(-1, name, 10, "info1", "info2")
        self.assertEqual(False, exists)

    def test_short_name_survey_choice(self):
        short_name = " "
        survey_name = "Survey service test 7 new survey"
        survey_id = sr.add_new_survey(survey_name)
        exists = ss.add_survey_choice(survey_id, short_name, 10, "info1", "info2")
        self.assertEqual(False, exists)

    def test_add_survey_choice(self):  
        survey_name = "Survey service test 8 new survey"
        survey_id = sr.add_new_survey(survey_name)
        name = "Testien kirjoittaminen on 6/5"
        exists = ss.add_survey_choice(survey_id, name, 10, "info1", "info2")
        self.assertEqual(True, exists)

    def test_get_invalid_survey_choice(self):
        exists = ss.get_survey_choice(-1)
        self.assertEqual(False, exists)
