import pytest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as sor
from src.entities.user import User
from src.tools.db_tools import clear_database



@pytest.fixture(autouse=True)
def setup_env():
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
    user3 = User("trt enjoyer", "ttrt@tester.com", True)
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



def test_add_owner_to_survey(setup_env):
    """
    Test that adding an owner to a survey works. Also test if owner added to survey
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    success_add = sor.add_owner_to_survey(survey_id, d["user_id"])
    assert success_add is True
    owner = sor.check_if_owner_in_survey(survey_id, d["user_id"])
    assert owner.survey_id == survey_id

def test_add_owner_invalid_survey(setup_env):
    """
    Test that you cannot add a owner to an invalid survey
    """
    d = setup_env
    success_add = sor.add_owner_to_survey("ITSNOTREAL", d["user_id"])
    assert success_add is False

def test_get_owner_invalid_survey():
    """
    Test that you cannot get an invalid owner from an invalid survey
    """
    success_get = sor.check_if_owner_in_survey("ITSNOTREAL", -1)
    assert success_get is False

def test_exceptions(setup_env):
    """
    Test that exceptions return False
    """
    d = setup_env
    success = sor.add_owner_to_survey(-1, d["user_id"])
    assert not success
    success = sor.check_if_owner_in_survey(-1, d["user_id"])
    assert not success
