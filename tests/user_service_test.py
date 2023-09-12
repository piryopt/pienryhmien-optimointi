import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.services.user_service import user_service as us
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database


class TestUserService(unittest.TestCase):

    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()
        clear_database()
        self.setup_user()

    def setup_user(self):
        self.ur = ur
        user1 = User("Tiina Testiopettaja", "tiina.testiope@email.com", True)
        self.ur.register(user1)

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_create_user_function_regognizes_email_in_use(self):
        '''
        Tests that the create_user() function notices when the app tries to
        register someone new with email that is already in use for another user.
        If user is accepted, the function return user. If not, returns None.
        '''
        result = us.create_user("Etunimi Sukunimi", "tiina.testiope@email.com", True)
        self.assertIsNone(result)

    def test_create_user_returns_false_if_not_validate(self):
        """
        Test that create_user() returns False if validate() returns false
        """
        result = us.create_user("", "tiina.testiope@email.com", True)
        self.assertEqual(result, False)

    def test_validate(self):
        """
        Test that validate returns true if name valid
        """
        result = us.validate("Testi Opettaja")
        self.assertEqual(result, True)

    def test_check_credentials_empty_email(self):
        '''
        Tests that check_credentials() function checks emails
        and notices if the email address provided is empty.
        Is expected to return False.
        '''
        empty_email = ""
        result = us.check_credentials(empty_email)
        self.assertFalse(result)

    def test_check_credentials_incorrect_email(self):
        '''
        Tests that check_credentials() function checks emails
        and notices if the email address provided is not correct.
        Is expected to return False.
        '''
        incorrect_email = "this_is_not_email"
        result = us.check_credentials(incorrect_email)
        self.assertFalse(result)

    def test_get_email_function_rejects_incorrect_id(self):
        '''
        Tests that the get_email() function correctly notices
        if provided id is not an integer, and returns False.
        '''
        test_list = []
        incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, test_list]
        for item in incorrect_ids:
            result = us.get_email(item)
            self.assertFalse(result)

    def test_get_email_function_returns_correct_email(self):
        '''
        Tests that the get_email() function returnsa correct email
        when given user id.
        '''
        test_user = User("Maija Poppanen", "maija@poppanen.com", True)
        self.ur.register(test_user)
        user_id = ur.find_by_email(test_user.email)[0]
        result = us.get_email(user_id)
        self.assertEqual(result, "maija@poppanen.com")

    def test_get_name_function_rejects_incorrect_name(self):
        '''
        Tests that the get_name() function correctly notices
        if provided id is not an integer, and returns False.
        '''
        test_list = []
        incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, test_list]
        for item in incorrect_ids:
            result = us.get_name(item)
            self.assertFalse(result)

    def test_get_name_function_returns_correct_name(self):
        '''
        Tests that the get_email() function returnsa correct email
        when given user id.
        '''
        test_user = User("Matti Meikäläinen", "matti@email.com", True)
        self.ur.register(test_user)
        user_id = ur.find_by_email(test_user.email)[0]
        result = us.get_name(user_id)
        self.assertEqual(result, "Matti Meikäläinen")

    def test_find_by_email_rejects_incorrect_email(self):
        '''
        Tests that the find_by_email() function correctly notices
        if provided email is not a string, and returns False.
        '''
        test_list = []
        incorrect_ids = ["", 3.14, 55, 9999999999, False, True, test_list]
        for item in incorrect_ids:
            result = us.find_by_email(item)
            self.assertFalse(result)

    def test_check_if_teacher_correct(self):
        '''
        Tests that the check_if_teacher() function returns correctly
        is user is a teacher.
        '''
        test_user = User("Pekka Virtanen", "pekka@email.com", True)
        self.ur.register(test_user)
        user_id = ur.find_by_email(test_user.email)[0]
        result = us.check_if_teacher(user_id)
        self.assertTrue(result)

    def test_len_all_students(self):
        """
        Tests that the length of the list of all students is correct
        """
        ur.register(User("1.3 keskiarvo", "muhlu@email.com", False))
        ur.register(User("motivaatio", "moti@email.com", False))
        ur.register(User("Jaloissa ei ole tuntoa", "weak.af@email.com", False))
        users = us.len_all_students()
        self.assertEqual(users, 3)

    def test_len_all_teachers(self):
        """
        Tests that the length of the list of all teachers is correct
        """
        users = us.len_all_teachers()
        self.assertEqual(users, 1)
