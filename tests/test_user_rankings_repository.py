
import os
import pytest
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as sor
from src.entities.user import User
from src.tools.db_tools import clear_database

@pytest.fixture
def setup_db():
    """
    Pytest fixture to set up and tear down Flask app and database for user rankings repository tests.
    """
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()
    clear_database()

    user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
    user2 = User("Not on anabolic", "anabolic@tester.com", True)
    ur.register(user1)
    ur.register(user2)
    user_id = ur.find_by_email(user1.email)[0]
    user_id2 = ur.find_by_email(user2.email)[0]
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, user_id)
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(user_id, survey_id, ranking, "", "")

    yield {
        "user_id": user_id,
        "user_id2": user_id2,
        "survey_id": survey_id,
        "ranking": ranking
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()

def test_add_user_ranking_returns_false_if_user_id_not_correct(setup_db):
    """
    Tests that add_user_ranking() returns false if adding ranking fails
    """
    user_id = setup_db["user_id"]
    survey_id = setup_db["survey_id"]
    ranking = setup_db["ranking"]
    success = urr.add_user_ranking(user_id + 12, survey_id, ranking, "", "")
    assert success is False

def test_get_user_ranking(setup_db):
    """
    Test that getting a user ranking from the database works
    """
    user_id = setup_db["user_id"]
    survey_id = setup_db["survey_id"]
    ranking = setup_db["ranking"]
    db_ranking = urr.get_user_ranking(user_id, survey_id).ranking
    assert db_ranking == ranking

def test_get_invalid_user_ranking(setup_db):
    """
    Test that getting an invalid user ranking from the database works correctly
    """
    user_id = setup_db["user_id"]
    exists = urr.get_user_ranking(user_id, -1)
    assert exists is False

def test_delete_user_ranking(setup_db):
    """
    Test that deleting a user ranking works
    """
    user_id = setup_db["user_id"]
    survey_id = setup_db["survey_id"]
    urr.delete_user_ranking(user_id, survey_id)
    deleted = urr.get_user_ranking(user_id, survey_id)
    assert deleted is False

def test_user_ranking_rejections(setup_db):
    """
    Test that rejections are correctly placed into the database, when a ranking contains them
    """
    user_id2 = setup_db["user_id2"]
    survey_id = setup_db["survey_id"]
    ranking = "2,3,5,4,1,6"
    rejections = "9,8"
    reason = "Because seven ate nine"
    urr.add_user_ranking(user_id2, survey_id, ranking, rejections, reason)
    db_rejections = urr.get_user_ranking(user_id2, survey_id).rejections
    assert db_rejections == rejections

def test_exceptions(setup_db):
    """
    Test that exceptions return False
    """
    user_id = setup_db["user_id"]
    success = urr.delete_user_ranking(user_id, -1)
    assert not success
