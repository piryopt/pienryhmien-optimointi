import os
import pytest
from flask import Flask
from dotenv import load_dotenv
from flask_babel import Babel
from src import db
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database


@pytest.fixture
def setup_db():
    """
    Pytest fixture to set up and tear down Flask app and database.
    """

    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    app.config["BABEL_DEFAULT_LOCALE"] = "fi"

    db.init_app(app)
    Babel(app)

    app_context = app.app_context()
    app_context.push()

    clear_database()

    user1 = User("Tiina Testiopettaja", "tiina.testiope@email.com", True)
    user2 = User("Maija Mallikas", "maija@tester.com", True)
    user3 = User("Tero Testaaja", "tero@tester.com", True)

    ur.register(user1)
    ur.register(user2)
    ur.register(user3)
    user_id = ur.find_by_email(user1.email)[0]
    user_id2 = ur.find_by_email(user2.email)[0]
    user_id3 = ur.find_by_email(user3.email)[0]

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "user_id2": user_id2,
        "user_id3": user_id3,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()
