import unittest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as sor
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestUserRankingsRepository(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        self.app.config["BABEL_DEFAULT_LOCALE"] = "fi"

        babel = Babel(self.app)

        def get_locale():
            return 'fi'

        babel.init_app(self.app, locale_selector=get_locale)
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
        sor.add_owner_to_survey(self.survey_id, self.user_id)
        self.ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id, self.survey_id, self.ranking, "", "")

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_add_user_ranking_returns_false_if_user_id_not_correct(self):
        """
        Tests that add_user_ranking() returns false if adding ranking fails
        """
        success = urr.add_user_ranking(self.user_id+12, self.survey_id, self.ranking, "", "")
        self.assertEqual(success, False)

    def test_get_user_ranking(self):
        """
        Test that getting a user ranking from the database works
        """
        db_ranking = urr.get_user_ranking(self.user_id, self.survey_id).ranking
        self.assertEqual(db_ranking, self.ranking)

    def test_get_invalid_user_ranking(self):
        """
        Test that getting an invalid user ranking from the database works correctly
        """
        exists = urr.get_user_ranking(self.user_id, -1)
        self.assertEqual(exists, False)

    def test_delete_user_ranking(self):
        """
        Test that deleting a user ranking works
        """
        urr.delete_user_ranking(self.user_id, self.survey_id)
        deleted = urr.get_user_ranking(self.user_id, self.survey_id)
        self.assertEqual(deleted, False)

    def test_user_ranking_rejections(self):
        """
        Test that rejections are correctly placed into the database, when a ranking contains them
        """
        ranking = "2,3,5,4,1,6"
        rejections = "9,8"
        reason = "Because seven ate nine"
        urr.add_user_ranking(self.user_id2, self.survey_id, ranking, rejections, reason)
        db_rejections = urr.get_user_ranking(self.user_id2, self.survey_id).rejections
        self.assertEqual(db_rejections, rejections)

    def test_exceptions(self):
        """
        Test that exceptions return False
        """
        success = urr.delete_user_ranking(self.user_id, -1)
        self.assertFalse(success)
