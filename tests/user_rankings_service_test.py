import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.user_repository import user_repository as ur
from src.services.survey_service import survey_service as ss
from src.services.survey_owners_service import survey_owners_service as sos
from src.services.user_rankings_service import user_rankings_service as urs
from src.entities.user import User
from src.tools.db_tools import clear_database
import json

class TestUserRankingsService(unittest.TestCase):
    def setUp(self):
        """
        Creates environment, test users and imports a test survey from json.
        """

        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        clear_database()

        user = User("Maija Mallikas", "maija@tester.com", True)
        user2 = User("Tero Testaaja", "tero@tester.com", True)
        ur.register(user)
        ur.register(user2)
        self.user_id = ur.find_by_email(user.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]
        self.user_email = user.email

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        self.survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"], 1, "01.01.2024", "02:02")
        sos.add_owner_to_survey(self.survey_id, self.user_email)

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_add_user_ranking(self):
        """
        Test that a user ranking can be submitted
        """
        success = urs.add_user_ranking(self.user_id, self.survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
        self.assertTrue(success)

    def test_add_user_invalid_ranking(self):
        """
        Test that an invalid user ranking cannot be submitted
        """
        success = urs.add_user_ranking(self.user_id, -1, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
        self.assertFalse(success)

    def test_user_ranking_exists(self):
        """
        Test that a correct user ranking can be returned
        """
        success = urs.add_user_ranking(self.user_id, self.survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
        self.assertTrue(success)
        ranking = urs.user_ranking_exists(self.survey_id, self.user_id)
        self.assertEqual(ranking.ranking, "1,2,3,4,5,6,7,8")
        self.assertEqual(ranking.rejections, "9")
        self.assertEqual(ranking.reason, "Because seven ate nine")

    def test_user_ranking_exists_invalid(self):
        """
        Test that an invalid ranking cannot be returned
        """
        ranking = urs.user_ranking_exists(-1, self.user_id)
        self.assertFalse(ranking)

    def test_delete_invalid_ranking(self):
        """
        Test that an invalid ranking cannot be deleted
        """
        success = urs.delete_ranking(-1, self.user_id)
        self.assertFalse(success)

    def test_delete_ranking(self):
        """
        Test that a ranking can be deleted
        """
        success = urs.add_user_ranking(self.user_id, self.survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
        self.assertTrue(success)
        success = urs.delete_ranking(self.survey_id, self.user_id)
        self.assertTrue(success)
        ranking = urs.user_ranking_exists(self.survey_id, self.user_id)
        self.assertFalse(ranking)

    def test_get_user_ranking(self):
        """
        Test that a ranking can be returned (Only the ranking)
        """
        success = urs.add_user_ranking(self.user_id, self.survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
        self.assertTrue(success)
        ranking = urs.get_user_ranking(self.user_id, self.survey_id)
        self.assertEqual(ranking, "1,2,3,4,5,6,7,8")

    def test_len_all_rankings(self):
        """
        Test the length of all created rankings
        """
        rankings_length = urs.len_all_rankings()
        self.assertEqual(rankings_length, 0)
        success = urs.add_user_ranking(self.user_id, self.survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
        self.assertTrue(success)
        rankings_length = urs.len_all_rankings()
        self.assertEqual(rankings_length, 1)
