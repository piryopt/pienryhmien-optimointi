
import pytest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.repositories.survey_owners_repository import survey_owners_repository as sor
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime


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

def test_get_survey(setup_env):
    """
    Create new survey and test if it exists and also test if the surveyname exists
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    survey = sr.get_survey(survey_id)
    assert survey[0] == survey_id

def test_check_that_survey_doesnt_exist():
    """
    Test that survey with invalid id doesn't exist
    """
    exists = sr.get_survey("ITSNOTREAL")
    assert exists is False

def test_survey_name_doesnt_exist(setup_env):
    """
    Test that surveyname doesn't exist
    """
    d = setup_env
    survey_name = "Test survey 2"
    exists = sr.survey_name_exists(survey_name, d["user_id"])
    assert exists is False

def test_count_created_surveys(setup_env):
    """
    Test that the number of created surveys is correct
    """
    d = setup_env
    survey_id1 = sr.create_new_survey("Test survey 3", 10, "Motivaatio", "2024-01-01 02:02")
    survey_id2 = sr.create_new_survey("Test survey 4", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id1, d["user_id2"])
    sor.add_owner_to_survey(survey_id2, d["user_id2"])
    count = sr.count_created_surveys(d["user_id2"])
    assert count == 2

def test_close_survey(setup_env):
    """
    Test that closing a survey works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 5", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id2"])
    sr.close_survey(survey_id)
    closed = sr.get_survey(survey_id).closed
    assert closed is True

def test_get_active_surveys(setup_env):
    """
    Test that getting a list of active surveys works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 6", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id2"])
    active_list = sr.get_active_surveys(d["user_id2"])
    assert len(active_list) == 1

def test_get_closed_surveys(setup_env):
    """
    Test that getting a list of closed surveys works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 7", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id2"])
    sr.close_survey(survey_id)
    closed_list = sr.get_closed_surveys(d["user_id2"])
    assert len(closed_list) == 1

def test_open_survey(setup_env):
    """
    Test that closing a survey works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 8", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    sr.close_survey(survey_id)
    closed = sr.get_survey(survey_id).closed
    assert closed is True
    sr.open_survey(survey_id)
    opened = sr.get_survey(survey_id).closed
    assert opened is False

def test_survey_name_exists(setup_env):
    """
    Test that a survey name exists when a survey is added to the database
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 9", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    exists = sr.survey_name_exists("Test survey 9", d["user_id"])
    assert exists is True

def test_count_created_surveys_invalid_id():
    """
    Test that the function behaves correctly when trying to get the list of all created surveys for an invalid user
    """
    exists = sr.count_created_surveys(-1)
    assert exists is False

def test_count_active_surveys_invalid_id():
    """
    Test that the function behaves correctly when trying to get the list of active created surveys for an invalid user
    """
    exists = sr.get_active_surveys(-1)
    assert exists is False

def test_survey_description(setup_env):
    """
    Test that getting the description of a survey works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 10", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    desc = sr.get_survey_description(survey_id)
    assert desc == "Motivaatio"

def test_survey_answered(setup_env):
    """
    Test that updating a survey so that it has its results saved works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 11", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    sr.update_survey_answered(survey_id)
    answered = sr.get_survey(survey_id).results_saved
    assert answered is True

def test_survey_time_end_correct(setup_env):
    """
    Test that the ending time of a created survey is correct
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 13", 10, "Ei motivaatiota", "2024-06-19 12:01")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    time = sr.get_survey_time_end(survey_id)
    assert time == datetime.datetime(2024, 6, 19, 12, 1)

def test_get_list_active_answered(setup_env):
    """
    Test that the list of active surveys which the student has answered is the correct length
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 14", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking, "", "")
    active_answered = sr.get_list_active_answered(d["user_id3"])
    assert len(active_answered) == 1

def test_get_list_closed_answered(setup_env):
    """
    Test that the list of closed surveys which the student has answered is the correct length
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking, "", "")
    sr.close_survey(survey_id)
    closed_answered = sr.get_list_closed_answered(d["user_id3"])
    assert len(closed_answered) == 1

def test_get_list_active_answered_invalid():
    """
    Test that getting the list of active surveys of an invalid account works
    """
    active_answered = sr.get_list_active_answered(-1)
    assert active_answered is False

def test_get_list_closed_answered_invalid():
    """
    Test that getting the list of closed surveys of an invalid account works
    """
    closed_answered = sr.get_list_closed_answered(-1)
    assert closed_answered is False

def test_get_list_all_open_surveys(setup_env):
    """
    Test that the amount of all open surveys is correct. The database is emptied before the test
    """
    d = setup_env
    clear_database()
    # re-create users after clearing db
    user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
    user2 = User("Not on anabolic", "anabolic@tester.com", True)
    ur.register(user1)
    ur.register(user2)
    user_id = ur.find_by_email(user1.email)[0]
    user_id2 = ur.find_by_email(user2.email)[0]
    survey_id1 = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id1, user_id)
    survey_id2 = sr.create_new_survey("Test survey 16", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id2, user_id2)
    survey_id3 = sr.create_new_survey("Test survey 17", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id3, user_id)
    sr.close_survey(survey_id3)
    all_open_surveys = sr.get_all_active_surveys()
    assert len(all_open_surveys) == 2

def test_save_survey_edit(setup_env):
    """
    Test that editing a survey works
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    sr.save_survey_edit(survey_id, "Edited survey", "moti", "2024-01-01 02:02")
    survey = sr.get_survey(survey_id)
    assert survey.surveyname == "Edited survey"
    assert survey.survey_description == "moti"

def test_get_survey_min_choices(setup_env):
    """
    Test that the min choices of a survey is correct
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, d["user_id"])
    min_choices = sr.get_survey_min_choices(survey_id)
    assert min_choices == 10

def test_get_survey_max_denied_choices(setup_env):
    """
    Test that the max denied choices is correct
    """
    d = setup_env
    survey_id = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2024-01-01 02:02", 2)
    sor.add_owner_to_survey(survey_id, d["user_id"])
    max_denied_choices = sr.get_survey_max_denied_choices(survey_id)
    assert max_denied_choices == 2

def test_exceptions():
    """
    Test that exceptions return False
    """
    success = sr.get_survey(-1)
    assert not success
    success = sr.survey_name_exists("Motivaatio", -1)
    assert not success
    success = sr.count_created_surveys(-1)
    assert not success
    success = sr.close_survey(-1)
    assert not success
    success = sr.open_survey(-1)
    assert not success
    success = sr.get_active_surveys(-1)
    assert not success
    success = sr.get_closed_surveys(-1)
    assert not success
    success = sr.update_survey_answered(-1)
    assert not success
    success = sr.get_survey_description(-1)
    assert not success
    success = sr.get_survey_time_end(-1)
    assert not success
    success = sr.get_survey_min_choices(-1)
    assert not success
    success = sr.get_survey_max_denied_choices(-1)
    assert not success
    success = sr.get_survey_search_visibility(-1)
    assert not success
