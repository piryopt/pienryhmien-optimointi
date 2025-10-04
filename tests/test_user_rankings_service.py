
import os
import pytest
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.repositories.user_repository import user_repository as ur
from src.services.survey_service import survey_service as ss
from src.services.survey_owners_service import survey_owners_service as sos
from src.services.user_rankings_service import user_rankings_service as urs
from src.entities.user import User
from src.tools.db_tools import clear_database
import json

@pytest.fixture
def setup_env():
    """
    Pytest fixture to set up and tear down Flask app, Babel, database, users, and survey for user rankings service tests.
    """
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

    user = User("Maija Mallikas", "maija@tester.com", True)
    user2 = User("Tero Testaaja", "tero@tester.com", True)
    ur.register(user)
    ur.register(user2)
    user_id = ur.find_by_email(user.email)[0]
    user_id2 = ur.find_by_email(user2.email)[0]
    user_email = user.email

    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    survey_id = ss.create_new_survey_manual(
        json_object["choices"], json_object["surveyGroupname"], user_id, json_object["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, user_email)

    yield {
        "user_id": user_id,
        "user_id2": user_id2,
        "user_email": user_email,
        "survey_id": survey_id
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()

def test_add_user_ranking(setup_env):
    """
    Test that a user ranking can be submitted
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    success = urs.add_user_ranking(user_id, survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
    assert success

def test_add_user_invalid_ranking(setup_env):
    """
    Test that an invalid user ranking cannot be submitted
    """
    user_id = setup_env["user_id"]
    success = urs.add_user_ranking(user_id, -1, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
    assert not success

def test_user_ranking_exists(setup_env):
    """
    Test that a correct user ranking can be returned
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    success = urs.add_user_ranking(user_id, survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
    assert success
    ranking = urs.user_ranking_exists(survey_id, user_id)
    assert ranking.ranking == "1,2,3,4,5,6,7,8"
    assert ranking.rejections == "9"
    assert ranking.reason == "Because seven ate nine"

def test_user_ranking_exists_invalid(setup_env):
    """
    Test that an invalid ranking cannot be returned
    """
    user_id = setup_env["user_id"]
    ranking = urs.user_ranking_exists(-1, user_id)
    assert not ranking

def test_delete_invalid_ranking(setup_env):
    """
    Test that an invalid ranking cannot be deleted
    """
    user_id = setup_env["user_id"]
    success = urs.delete_ranking(-1, user_id)
    assert not success

def test_delete_ranking(setup_env):
    """
    Test that a ranking can be deleted
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    success = urs.add_user_ranking(user_id, survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
    assert success
    success = urs.delete_ranking(survey_id, user_id)
    assert success
    ranking = urs.user_ranking_exists(survey_id, user_id)
    assert not ranking

def test_get_user_ranking(setup_env):
    """
    Test that a ranking can be returned (Only the ranking)
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    success = urs.add_user_ranking(user_id, survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
    assert success
    ranking = urs.get_user_ranking(user_id, survey_id)
    assert ranking == "1,2,3,4,5,6,7,8"

def test_len_all_rankings(setup_env):
    """
    Test the length of all created rankings
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    rankings_length = urs.len_all_rankings()
    assert rankings_length == 0
    success = urs.add_user_ranking(user_id, survey_id, "1,2,3,4,5,6,7,8", "9", "Because seven ate nine")
    assert success
    rankings_length = urs.len_all_rankings()
    assert rankings_length == 1
