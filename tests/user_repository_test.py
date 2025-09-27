import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database


class TestUserRepository(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()
        clear_database()
        self.ur = ur
        self.user1 = User("Tiina Testiopettaja", "tiina.testiope@email.com", True)
        self.ur.register(self.user1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_user_by_email_invalid(self):
        """
        Test that an invalid email returns False
        """
        user = ur.get_user_by_email("moti@motivaatio.com")
        self.assertFalse(user)

    def test_get_user_by_email(self):
        """
        Test that a user is returned with the correct email
        """
        user = ur.get_user_by_email("tiina.testiope@email.com")
        self.assertEqual(user.name, "Tiina Testiopettaja")
        self.assertEqual(user.email, "tiina.testiope@email.com")
        self.assertTrue(user.isteacher)
