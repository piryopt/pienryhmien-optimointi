import pytest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
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
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    so.add_owner_to_survey(survey_id, user_id)
    choice_id = scr.create_new_survey_choice(survey_id, "choice 1", 10, 5, False)
    choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 5, False)

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "user_id2": user_id2,
        "survey_id": survey_id,
        "choice_id": choice_id,
        "choice_id2": choice_id2,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()



def test_find_survey_choices(setup_env):
    """
    Test that the lenght of a list of survey choices for a survey is correct
    """
    d = setup_env
    choice_list = scr.find_survey_choices(d["survey_id"])
    assert len(choice_list) == 2

def test_get_survey_choice(setup_env):
    """
    Test that getting a survey choice works
    """
    d = setup_env
    choice = scr.get_survey_choice(d["choice_id"])
    assert choice.name == "choice 1"

def test_get_survey_choice_returns_false_forn_nonexistant_choice(setup_env):
    """
    Test that getting a survey choice returns False if choice doesn't exist
    """
    d = setup_env
    choice = scr.get_survey_choice(d["choice_id"] + 12)
    assert choice is False

def test_create_new_survey_choice_returns_false_for_exception():
    """
    Test that a survey choice is not added if there's an error in survey id
    and that return is False
    """
    success = scr.create_new_survey_choice("not a survey", "choice 1", 10, 5, False)
    assert success is False

def test_get_invalid_choice():
    """
    Test that getting an invalid survey choice behaves the correct way
    """
    choice = scr.get_survey_choice("ITSNOTREAL")
    assert choice is False

def test_edit_choice_group_size(setup_env):
    """
    Tests that group size is edited and the correct group size saved
    """
    d = setup_env
    success = scr.edit_choice_group_size(d["survey_id"], "choice 1", 5)
    assert success is True
    new_size = scr.get_survey_choice(d["choice_id"])
    assert new_size.max_spaces == 5

def test_create_new_choice_info(setup_env):
    """
    Test that create_new_choice_info() works and returns True
    """
    d = setup_env
    success = scr.create_new_choice_info(d["choice_id"], "Priority", "5", False)
    assert success is True

def test_create_new_choice_info_not_working_with_false_choice_id(setup_env):
    """
    Test that create_new_choice_info() works and returns True
    """
    d = setup_env
    success = scr.create_new_choice_info(d["choice_id"] + 56, "Priority", "0", False)
    assert success is False

def test_get_choice_additional_infos(setup_env):
    """
    Test that getting the additional info of a survey choice works
    """
    d = setup_env
    scr.create_new_choice_info(d["choice_id"], "Moti", "Vaatio", False)
    info = scr.get_choice_additional_infos(d["choice_id"])
    assert info[0].info_key == "Moti"
    assert info[0].info_value == "Vaatio"

def test_get_all_additional_infos(setup_env):
    """
    Adds additional info on two choices and checks that returned
    number of infos is correct
    """
    d = setup_env
    scr.create_new_choice_info(d["choice_id"], "Priority", "4", False)
    scr.create_new_choice_info(d["choice_id2"], "Priority", "11", False)
    info = scr.get_all_additional_infos(d["survey_id"])
    assert len(info) == 2

def test_get_all_additional_infos_not_hidden(setup_env):
    """
    Adds additional info on two choices and checks that returned
    number of infos is correct
    """
    d = setup_env
    scr.create_new_choice_info(d["choice_id"], "Osoite", "Kakkakuja 4", False)
    scr.create_new_choice_info(d["choice_id"], "Kaupunki", "Helsinki", True)
    info = scr.get_choice_additional_infos_not_hidden(d["choice_id"])
    assert len(info) == 1
    assert info[0][0] == "Osoite"
    assert info[0][1] == "Kakkakuja 4"

def test_exceptions():
    """
    Test that exceptions return False
    """
    success = scr.find_survey_choices(-1)
    assert not success
    success = scr.get_all_additional_infos(-1)
    assert not success
