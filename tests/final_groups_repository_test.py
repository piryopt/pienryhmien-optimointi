import unittest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.final_group_repository import final_group_repository as fgr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as so
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestFinalGroupsRepository(unittest.TestCase):
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

    def test_save_result(self):
        """
        Test that the results are saved into the database
        """
        survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 01:01.00")
        so.add_owner_to_survey(survey_id, self.user_id)
        choice_id1 = scr.create_new_survey_choice(survey_id, "choice 1", 10, 1)
        choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 1)
        
        success = fgr.save_result(self.user_id, survey_id, choice_id2)
        self.assertEqual(success, True)

    def test_result_not_saved_if_user_not_found(self):
        survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 01:01.00")
        so.add_owner_to_survey(survey_id, self.user_id)
        choice_id1 = scr.create_new_survey_choice(survey_id, "choice 1", 10, 1)
        choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 1)
        
        success = fgr.save_result(self.user_id+12, survey_id, choice_id2)
        self.assertEqual(success, False)
    