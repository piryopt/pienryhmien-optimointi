import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestUserRankingsRepository(unittest.TestCase):
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

    def test_get_user_ranking(self):
        survey_id = sr.create_new_survey("Test survey 1", self.user_id, 10, "Motivaatio")
        ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id, survey_id, ranking)
        db_ranking = urr.get_user_ranking(self.user_id, survey_id).ranking
        self.assertEqual(db_ranking, ranking)

    def test_get_invalid_user_ranking(self):
        exists = urr.get_user_ranking(self.user_id, -1)
        self.assertEqual(exists, False)

    def test_delete_user_ranking(self):
        survey_id = sr.create_new_survey("Test survey 2", self.user_id, 10, "Motivaatio")
        ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id, survey_id, ranking)
        deleted = urr.get_user_ranking(self.user_id, survey_id).ranking
        urr.delete_user_ranking(self.user_id, survey_id)
        deleted = urr.get_user_ranking(self.user_id, survey_id)
        self.assertEqual(deleted, False)