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

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        user = User("Not on tren Testerr", 101010101, "tren4lyfe@tester.com", True)
        user2 = User("Hashtag natty", 101010101, "anabolics4lyfe@tester.com", True)
        ur.register(user)
        ur.register(user2)
        self.user_id = ur.find_by_email(user.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]

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
        
        test_survey1_id = sr.add_new_survey("Survey service test 1", self.user_id)
        for i in range(3):
            sr.add_new_survey_choice(test_survey1_id, "test" + str(i) + "choice", 10, "info1", "info2")
        choice_list = ss.get_list_of_survey_choices(test_survey1_id)
        self.assertEqual(3, len(choice_list))
        """

    def test_get_survey_name(self):
        """
        Test that a survey name is returned with a valid survey id
        """
        test_survey2_id = sr.add_new_survey("Survey service test 2", self.user_id)
        name = ss.get_survey_name(test_survey2_id)
        self.assertEqual(name, "Survey service test 2")

    def test_get_survey_name_nonexisting_id(self):
        """
        Test that no survey name is returned for an invalid survey id
        """
        name = ss.get_survey_name(-1)
        self.assertEqual(name, False)

    def test_user_ranking_doesnt_exist_and_cant_delete(self):
        """
        Test that a user ranking that doesn't exist cannot be deleted
        """
        test_survey3_id = sr.add_new_survey("Survey service test 3", self.user_id)
        exists = ss.user_ranking_exists(test_survey3_id, self.user_id)
        self.assertEqual(exists, False)
        deleted = ss.delete_ranking(test_survey3_id, self.user_id)
        self.assertEqual(False, deleted)


    def test_add_user_ranking_and_delete_it(self):
        """
        Test that a created user ranking can be deleted
        
        test_survey4_id = sr.add_new_survey("Survey service test 4", self.user_id)
        for i in range(3):
            sr.add_new_survey_choice(test_survey4_id, "test" + str(i) + "choice", 10, "info1", "info2")
        exists = ss.add_user_ranking(test_survey4_id, "1,2,3,4", self.user_id)
        self.assertEqual(True, exists)
        deleted = ss.delete_ranking(test_survey4_id, self.user_id)
        self.assertEqual(True, deleted)
        """

    def test_user_ranking_exists(self):
        """
        Test that a user ranking exists
        
        test_survey5_id = sr.add_new_survey("Survey service test 5", self.user_id)
        for i in range(3):
            sr.add_new_survey_choice(test_survey5_id, "test" + str(i) + "choice", 10, "info1", "info2")
        ss.add_user_ranking(test_survey5_id, "1,2,3,4", self.user_id)
        ranking = ss.user_ranking_exists(test_survey5_id, self.user_id)
        self.assertEqual("1,2,3,4", ranking[3])
        """

    def test_add_new_survey_name_exists(self):
        """
        Test that a survey with a identical name to a open survey cannot be created
        """
        name = "Survey service test 6 new survey"
        ss.add_new_survey(name, self.user_id)
        exists = ss.add_new_survey(name, self.user_id)
        self.assertEqual(False, exists)

    def test_short_name_new_survey(self):
        """
        Test that a survey with a name that is too short cannot be created
        """
        name = "asd"
        exists = ss.add_new_survey(name, self.user_id)
        self.assertEqual(False, exists)

    def test_add_invalid_survey_choice(self):
        """
        Test that a survey_choice cannot be added to a invalid survey
        """
        name = "Testien kirjoittaminen on 6/5"
        exists = ss.add_survey_choice(-1, name, 10, "info1", "info2")
        self.assertEqual(False, exists)

    def test_short_name_survey_choice(self):
        """
        Test that a survey_choice cannot have too short of a name
        """
        short_name = " "
        survey_name = "Survey service test 7 new survey"
        survey_id = sr.add_new_survey(survey_name, self.user_id)
        exists = ss.add_survey_choice(survey_id, short_name, 10, "info1", "info2")
        self.assertEqual(False, exists)

    def test_add_survey_choice(self):
        """
        Test that a valid survey_choice gets added
    
        survey_name = "Survey service test 8 new survey"
        survey_id = sr.add_new_survey(survey_name, self.user_id)
        name = "Testien kirjoittaminen on 6/5"
        exists = ss.add_survey_choice(survey_id, name, 10, "info1", "info2")
        self.assertEqual(True, exists)
        """

    def test_get_invalid_survey_choice(self):
        """
        Test that a invalid survey choice doen't exist
        """
        exists = ss.get_survey_choice(-1)
        self.assertEqual(False, exists)

    def test_create_survey_from_csv(self):
        ss.create_survey_from_csv("test_survey.csv", "AAAAAAA", 3)
        
    def test_count_surveys_created_invalid(self):
        """
        Test that an invalid user has no surveys created
        """
        count = ss.count_surveys_created(-1)
        self.assertEqual(0, count)

    def test_count_surveys_created(self):
        """
        Test that an invalid user has no surveys created
        """
        sr.add_new_survey("Motivaatio 1", self.user_id2)
        sr.add_new_survey("Motivaatio 2", self.user_id2)
        count = ss.count_surveys_created(self.user_id2)
        self.assertEqual(2, count)

    def test_close_survey(self):
        """
        Test that a survey can be closed
        """
        survey_id = sr.add_new_survey("Motivaatio 3", self.user_id)
        closed = ss.close_survey(survey_id, self.user_id)
        self.assertEqual(True, closed)

    def test_close_survey_wrong_id(self):
        """
        Test that a survey cannot be closed by someone who didn't create the survey
        """
        survey_id = sr.add_new_survey("Motivaatio 4", self.user_id)
        closed = ss.close_survey(survey_id, self.user_id2)
        self.assertEqual(False, closed)

    def test_close_invalid_survey(self):
        """
        Test that a survey that doesn't exist cannot be closed
        """
        closed = ss.close_survey(-1, self.user_id)
        self.assertEqual(False, closed)

    def test_get_active_surveys(self):
        """
        Test that the amount of active surveys is correct
        """
        survey_id = sr.add_new_survey("Motivaatio 3", self.user_id2)
        count = len(ss.get_active_surveys(self.user_id2))
        self.assertEqual(3, count)
        ss.close_survey(survey_id, self.user_id2)
        count = len(ss.get_active_surveys(self.user_id2))
        self.assertEqual(2, count)

    def test_check_if_survey_closed(self):
        """
        Check that closing a survey works
        """
        survey_id = sr.add_new_survey("Motivaatio 6", self.user_id)
        ss.close_survey(survey_id, self.user_id)
        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(True, closed)

    def test_check_if_survey_closed_invalid(self):
        """
        Check that an invalid survey cannot be closed
        """
        closed = ss.check_if_survey_closed(-1)
        self.assertEqual(False, closed)

    def test_get_list_closed_surveys(self):
        """
        Test that the amount of closed surveys is correct
        """
        survey_id = sr.add_new_survey("Motivaatio 7", self.user_id2)
        ss.close_survey(survey_id, self.user_id2)
        count = len(ss.get_list_closed_surveys(self.user_id2))
        self.assertEqual(2, count)

