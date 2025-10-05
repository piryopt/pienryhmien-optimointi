import os
import pytest
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database


@pytest.fixture
def test_app():
    """
    Pytest fixture to set up and tear down Flask app and database for user repository tests.
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
    yield app  # yield allows test to run after setup, before teardown
    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_get_user_by_email_invalid(test_app):
    """
    Test that an invalid email returns False
    """
    user = ur.get_user_by_email("moti@motivaatio.com")
    assert not user


def test_get_user_by_email(test_app):
    """
    Test that a user is returned with the correct email
    """
    user = ur.get_user_by_email("tiina.testiope@email.com")
    assert user.name == "Tiina Testiopettaja"
    assert user.email == "tiina.testiope@email.com"
    assert user.isteacher


def test_get_user_data_returns_false_for_invalid_id(test_app):
    """
    Test that get_user_data() returns False if user not found or id invalid
    """

    incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, []]
    for item in incorrect_ids:
        assert ur.get_user_data(item) is False


def test_change_user_language_returns_false_for_invalid_user_id(test_app):
    """
    Test that changing language with an invalid user id returns False
    """
    incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, []]
    for item in incorrect_ids:
        assert ur.change_user_language(item, "en") is False
