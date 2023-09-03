import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.feedback_repository import feedback_repository as fr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database

class TestFeedbackRepository(unittest.TestCase):
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
        user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
        self.ur.register(user1)
        self.user_id = ur.find_by_email(user1.email)[0]

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_new_feedback(self):
        """
        Test that creating new feedback works
        """
        success = fr.new_feedback(self.user_id, "Testi palaute 1", "bugi", "Toimiiko eka testi?")
        self.assertTrue(success)

    def test_get_feedbacK(self):
        """
        Test that getting a valid feedback works
        """
        feedback_id = ""
        fr.new_feedback(self.user_id, "Testi palaute 2", "bugi", "Toimiiko toka testi?")
        feedback_list = fr.get_unsolved_feedback()
        for f in feedback_list:
            if f.title == "Testi palaute 2":
                feedback_id = f.id
        feedback = fr.get_feedback(feedback_id)
        self.assertEqual(feedback.title, "Testi palaute 2")

    def test_get_invalid_feedbacK(self):
        """
        Test that getting a invalid feedback works
        """
        success = fr.get_feedback(-1)
        self.assertFalse(success)

    def test_get_unsolved_feedback(self):
        """
        Test that the list of unsolved feedback is the correct size
        """
        fr.new_feedback(self.user_id, "Testi palaute 5", "bugi", "Toimiiko 5. testi?")
        unsolved_list = fr.get_unsolved_feedback()
        self.assertEqual(1, len(unsolved_list))

    def test_mark_feedback_solved(self):
        """
        Test that closing a feedback works and that the list of solved feedback is the correct size
        """
        fr.new_feedback(self.user_id, "Testi palaute 3", "bugi", "Toimiiko kolmas testi?")
        feedback_id = ""
        feedback_list = fr.get_unsolved_feedback()
        for f in feedback_list:
            if f.title == "Testi palaute 3":
                feedback_id = f.id
        success = fr.mark_feedback_solved(feedback_id)
        self.assertTrue(success)
        feedback = fr.get_feedback(feedback_id)
        self.assertTrue(feedback.solved)
        unsolved_list = fr.get_solved_feedback()
        self.assertEqual(1, len(unsolved_list))

    def test_check_unsolved_title_doesnt_exist(self):
        success = fr.check_unsolved_title_doesnt_exist(self.user_id, "Testi palaute 4")
        self.assertTrue(success)
        fr.new_feedback(self.user_id, "Testi palaute 4", "bugi", "Toimiiko 4. testi?")
        success = fr.check_unsolved_title_doesnt_exist(self.user_id, "Testi palaute 4")
        self.assertFalse(success)
