import os
import pytest
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.services.user_service import user_service as us
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database


@pytest.fixture
def test_app():
    """
    Pytest fixture to set up and tear down Flask app and database for user service tests.
    """
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()
    clear_database()
    user1 = User("Tiina Testiopettaja", "tiina.testiope@email.com", True)
    ur.register(user1)
    yield app
    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_create_user_function_regognizes_email_in_use(test_app):
    """
    Tests that the create_user() function notices when the app tries to
    register someone new with email that is already in use for another user.
    If user is accepted, the function return user. If not, returns None.
    """
    result = us.create_user("Etunimi Sukunimi", "tiina.testiope@email.com", True)
    assert result is None


def test_create_user_returns_false_if_not_validate(test_app):
    """
    Test that create_user() returns False if validate() returns false
    """
    result = us.create_user("", "tiina.testiope@email.com", True)
    assert result is False


def test_validate(test_app):
    """
    Test that validate returns true if name valid
    """
    result = us.validate("Testi Opettaja")
    assert result is True


def test_validate_retrurns_false_for_invalid_name(test_app):
    """
    Test that validate returns false if name invalid
    """
    result = us.validate("")
    assert result is False


def test_check_credentials_empty_email(test_app):
    """
    Tests that check_credentials() function checks emails
    and notices if the email address provided is empty.
    Is expected to return False.
    """
    empty_email = ""
    result = us.check_credentials(empty_email)
    assert not result


def test_check_credentials_incorrect_email(test_app):
    """
    Tests that check_credentials() function checks emails
    and notices if the email address provided is not correct.
    Is expected to return False.
    """
    incorrect_email = "this_is_not_email"
    result = us.check_credentials(incorrect_email)
    assert not result


def test_get_email_function_rejects_incorrect_id(test_app):
    """
    Tests that the get_email() function correctly notices
    if provided id is not an integer, and returns False.
    """
    test_list = []
    incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, test_list]
    for item in incorrect_ids:
        result = us.get_email(item)
        assert not result


def test_get_email_function_returns_correct_email(test_app):
    """
    Tests that the get_email() function returns correct email
    when given user id.
    """
    test_user = User("Maija Poppanen", "maija@poppanen.com", True)
    ur.register(test_user)
    user_id = ur.find_by_email(test_user.email)[0]
    result = us.get_email(user_id)
    assert result == "maija@poppanen.com"


def test_get_name_function_rejects_incorrect_name(test_app):
    """
    Tests that the get_name() function correctly notices
    if provided id is not an integer, and returns False.
    """
    test_list = []
    incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, test_list]
    for item in incorrect_ids:
        result = us.get_name(item)
        assert not result


def test_get_name_function_returns_correct_name(test_app):
    """
    Tests that the get_name() function returns correct name
    when given user id.
    """
    test_user = User("Matti Meikäläinen", "matti@email.com", True)
    ur.register(test_user)
    user_id = ur.find_by_email(test_user.email)[0]
    result = us.get_name(user_id)
    assert result == "Matti Meikäläinen"


def test_find_by_email_rejects_incorrect_email(test_app):
    """
    Tests that the find_by_email() function correctly notices
    if provided email is not a string, and returns False.
    """
    test_list = []
    incorrect_ids = ["", 3.14, 55, 9999999999, False, True, test_list]
    for item in incorrect_ids:
        result = us.find_by_email(item)
        assert not result


def test_check_if_teacher_correct(test_app):
    """
    Tests that the check_if_teacher() function returns correctly
    is user is a teacher.
    """
    test_user = User("Pekka Virtanen", "pekka@email.com", True)
    ur.register(test_user)
    user_id = ur.find_by_email(test_user.email)[0]
    result = us.check_if_teacher(user_id)
    assert result


def test_len_all_students(test_app):
    """
    Tests that the length of the list of all students is correct
    """
    ur.register(User("1.3 keskiarvo", "muhlu@email.com", False))
    ur.register(User("motivaatio", "moti@email.com", False))
    ur.register(User("Jaloissa ei ole tuntoa", "weak.af@email.com", False))
    users = us.len_all_students()
    assert users == 3


def test_len_all_students_when_no_students(test_app):
    """
    Tests that all_students() returns 0 when there are no students in the database
    """
    users = us.len_all_students()
    assert users == 0


def test_len_all_teachers(test_app):
    """
    Tests that the length of the list of all teachers is correct
    """
    users = us.len_all_teachers()
    assert users == 1


def test_get_user_id_by_email(test_app):
    """
    Test that the id of the user is returned when given the correct email
    """
    user_id = us.get_user_id_by_email("tiina.testiope@email.com")
    assert isinstance(user_id, int)


def test_get_user_id_by_invalid_email(test_app):
    """
    Test that no id is returned with an invalid email
    """
    user_id = us.get_user_id_by_email("moti@motivaatio.com")
    assert not user_id


def test_logout_clears_session(test_app):
    """
    Test that the logout function clears the session
    """
    with test_app.test_request_context():
        from flask import session

        session["email"] = "test@email.com"
        session["user_id"] = 1
        session["full_name"] = "Test User"
        session["role"] = "Opettaja"
        session["reloaded"] = False
        session["admin"] = True
        session["language"] = "fi"

        us.logout()

        for key in ["email", "user_id", "full_name", "role", "reloaded", "admin", "language"]:
            assert key not in session


def test_update_user_language_valid_language(test_app):
    """
    Test that update_user_language returns True if the language is valid and
    the session language is updated
    """
    user_id = us.get_user_id_by_email("tiina.testiope@email.com")

    with test_app.test_request_context():
        from flask import session

        session["language"] = "fi"
        result = us.update_user_language(user_id, "en")

    assert result

    user = ur.find_by_email("tiina.testiope@email.com")
    assert user.language == "en"


def test_update_user_language_invalid_language(test_app):
    """
    Test that update_user_language returns False if the language is invalid and
    the session language is not updated
    """
    user_id = us.get_user_id_by_email("tiina.testiope@email.com")

    with test_app.test_request_context():
        from flask import session

        session["language"] = "fi"
        result = us.update_user_language(user_id, "invalid_language")

    assert not result

    user = ur.find_by_email("tiina.testiope@email.com")
    assert user.language == "fi"
