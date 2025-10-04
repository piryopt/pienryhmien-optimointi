import pytest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.final_group_repository import final_group_repository as fgr
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_owners_repository import survey_owners_repository as so
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
    ur.register(user1)
    ur.register(user2)
    user_id = ur.find_by_email(user1.email)[0]
    user_id2 = ur.find_by_email(user2.email)[0]

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "user_id2": user_id2,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()

def test_save_result(setup_env):
    """
    Test that the results are saved into the database
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 01:01.00")
    so.add_owner_to_survey(survey_id, d["user_id"])
    choice_id1 = scr.create_new_survey_choice(survey_id, "choice 1", 10, 1, False)
    choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 1, False)

    success = fgr.save_result(d["user_id"], survey_id, choice_id2)
    assert success is True

def test_result_not_saved_if_user_not_found(setup_env):
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 01:01.00")
    so.add_owner_to_survey(survey_id, d["user_id"])
    choice_id1 = scr.create_new_survey_choice(survey_id, "choice 1", 10, 1, False)
    choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 1, False)

    success = fgr.save_result(d["user_id"] + 12, survey_id, choice_id2)
    assert success is False
