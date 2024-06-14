import unittest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.services.feedback_service import feedback_service as fs
from src.repositories.user_repository import user_repository as ur
from src.repositories.feedback_repository import feedback_repository as fr
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestFeedbackService(unittest.TestCase):
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

        user = User("Not on tren Testerr", "tren4lyfe@tester.com", True)
        ur.register(user)
        self.user_id = ur.find_by_email(user.email)[0]
        self.data = {}
        self.data["title"] = "Valitus testeistä"
        self.data["type"] = "muu"
        self.data["content"] = "Testikattavuus voisi olla parempi"

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_new_feedback(self):
        """
        Test that adding a new feedback works
        """
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertTrue(success)

    def test_new_feedback_title_exists(self):
        """
        Test that you cannot add a feedback if the title exists
        """
        self.data["title"] = "otsikko"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertTrue(success)
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertEqual(message, "Olet jo luonut palautteen tällä otsikolla!")

    def test_new_feedback_content_too_short(self):
        """
        Test that you cannot add feedback if the content is to short
        """
        self.data["title"] = "Valitus testeistä"
        self.data["content"] = "moti"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertFalse(success)
        self.assertEqual(message, "Sisältö on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 5.")

    def test_new_feedback_title_too_short(self):
        """
        Test that you cannot add feedback if the title is to short
        """
        self.data["title"] = "aa"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertFalse(success)
        self.assertEqual(message, "Otsikko on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 3.")

    def test_unsolved_list(self):
        """
        Test that the list of unsolved feedback is the correct size
        """
        self.data["title"] = "aaaaaaaaaa"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertTrue(success)
        self.data["title"] = "bbbbbbbbbb"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertTrue(success)
        feedback_list = fs.get_unsolved_feedback()
        self.assertEqual(2, len(feedback_list))

    def test_title_too_long(self):
        """
        Test that the title of a new feedback isn't too long
        """
        self.data["title"] = "a" * 51
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertFalse(success)

    def test_content_too_long(self):
        """
        Test that the content of a new feedback isn't too long
        """
        self.data["title"] = "Valitus testeistä"
        self.data["content"] = "testit ovat heikkoja! " * 100
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertFalse(success)

    def test_get_invalid_feedback(self):
        """
        Test that you cannot get an invalid feedback that hasn't been solved
        """
        success = fs.get_feedback(-1)
        self.assertFalse(success)

    def test_get_feedback(self):
        """
        Test that the data of an unsolved feedback is correct
        """
        self.data["title"] = "Testit ovat mahtavia!"
        self.data["content"] = "Huijasin, ne ovat heikkoja >:D"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertTrue(success)
        all_unsolved_feedback = fr.get_unsolved_feedback()
        feedback = all_unsolved_feedback[-1]
        feedback_data = fs.get_feedback(feedback.id)
        self.assertEqual(feedback_data[1], "Testit ovat mahtavia!")
        self.assertEqual(feedback_data[4], "Huijasin, ne ovat heikkoja >:D")

    def test_get_invalid_solved_feedback(self):
        """
        Test that you cannot get an invalid feedback that has been solved
        """
        solved_feedback = fs.get_solved_feedback()
        self.assertEqual(len(solved_feedback), 0)

    def test_get_solved_feedback(self):
        """
        Test that the data of a solved feedback is correct
        """
        self.data["title"] = "Testit ovat todella mahtavia!"
        self.data["content"] = "Huijasin, ne ovat heikkoja >:D"
        (success, message) = fs.new_feedback(self.user_id, self.data)
        self.assertTrue(success)
        all_unsolved_feedback = fr.get_unsolved_feedback()
        feedback = all_unsolved_feedback[-1]
        fs.mark_feedback_solved(feedback.id)
        all_solved_feedback = fs.get_solved_feedback()
        feedback_data = all_solved_feedback[-1]
        self.assertEqual(feedback_data[1], "Testit ovat todella mahtavia!")
