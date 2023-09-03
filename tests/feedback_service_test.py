import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.services.feedback_service import feedback_service as fs
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestFeedbackService(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
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
