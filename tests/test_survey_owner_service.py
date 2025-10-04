import pytest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.services.survey_owners_service import survey_owners_service as sos
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime
import json



@pytest.fixture(autouse=True)
def setup_env():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    app.config["BABEL_DEFAULT_LOCALE"] = "fi"

    babel = Babel(app)
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()

    clear_database()

    user = User("Not on tren Testerr", "tren4lyfe@tester.com", True)
    user2 = User("Hashtag natty", "anabolics4lyfe@tester.com", False)
    ur.register(user)
    ur.register(user2)
    user_id = ur.find_by_email(user.email)[0]
    user_email = user.email
    user_email_student = user2.email

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "user_email": user_email,
        "user_email_student": user_email_student,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()



def test_add_owner_to_survey(setup_env):
    """
    Test that adding a owner to a survey works and check that it cannot be added again
    """
    d = setup_env
    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    survey_id = ss.create_new_survey_manual(
        json_object["choices"], "Test survey 1", d["user_id"], json_object["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    success, message = sos.add_owner_to_survey(survey_id, d["user_email"])
    assert success is True
    success, message = sos.add_owner_to_survey(survey_id, d["user_email"])
    assert success is False

def test_add_owner_to_survey_invalid_email(setup_env):
    """
    Test that adding an email that isn't in the database works correctly
    """
    d = setup_env
    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    survey_id = ss.create_new_survey_manual(
        json_object["choices"], "Test survey 2", d["user_id"], json_object["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    success, message = sos.add_owner_to_survey(survey_id, "trt@tester.com")
    assert success is False

def test_add_owner_to_invalid_survey(setup_env):
    """
    Test that you cannot add a owner to an invalid survey
    """
    d = setup_env
    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    success, message = sos.add_owner_to_survey("ITSNOTREAL", d["user_email"])
    assert success is False
