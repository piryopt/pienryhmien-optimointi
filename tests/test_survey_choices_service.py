import pytest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.repositories.user_repository import user_repository as ur
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.services.survey_owners_service import survey_owners_service as sos
from src.entities.user import User
from src.tools.db_tools import clear_database
import json


@pytest.fixture(autouse=True)
def setup_env():
    """
    Creates environment, test users and imports a test survey from json.
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
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "user_id2": user_id2,
        "user_email": user_email,
        "survey_id": survey_id,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()


def test_get_list_of_survey_choices_returns_false_if_no_data_found():
    """
    Inputs a nonexistent survey id to getter and checks that return is "False"
    """
    ret = scs.get_list_of_survey_choices("ITSNOTREAL")
    assert ret is False


def test_get_list_of_survey_choices_returns_correct_number_of_choices(setup_env):
    """
    Tests that get_list_of_survey_choices() returns a list with two members
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    assert len(choices) == 2


def test_get_list_of_survey_choices_returns_correct_number_of_spaces(setup_env):
    """
    Tests that get_list_of_survey_choices() returns a list of choices where
    the sum of available spots matches the test data used
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    assert choices[0][3] + choices[1][3] == 14


def test_get_list_of_survey_choices_returns_correct_choice_names(setup_env):
    """
    Tests that get_list_of_survey_choices() returns a list of choices where
    the combined choice names matches the input data
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    assert choices[0][2] + " " + choices[1][2] == "Esimerkkipäiväkoti 1 Esimerkkipäiväkoti 2"


def test_get_survey_choice_returns_false_if_survey_not_found():
    """
    Tests that function get_survey_choice() returns false if no
    choice found with the id used as input, uses a string as input
    when ids should be int
    """
    assert scs.get_survey_choice("Not an id") is False


def test_get_survey_choice_gets_correct_choice(setup_env):
    """
    Fetches all choices with get_list_of_survey_choices() and inputs
    the first result choice id to function get_survey_choice(),
    then tests that the fetched choice names match
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    one_choice = scs.get_survey_choice(choices[0][0])
    assert choices[0][2] == one_choice[2]


def test_get_survey_choice_min_size(setup_env):
    """
    Fetches all choices with get_list_of_survey_choices() and inputs
    the first result choice id to function get_survey_choice_min_size(),
    then tests that the returned min_size value is correct
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    min_size = scs.get_survey_choice_min_size(choices[0].id)
    assert min_size == choices[0].min_size


def test_get_survey_choice_min_size_invalid_id():
    """
    Tests that function get_survey_choice_min_size returns False
    when an invalid id is used as input
    """
    assert scs.get_survey_choice_min_size("Not an id") is False


def test_get_choice_name_and_spaces_gets_correct_choice(setup_env):
    """
    Fetches all choices with get_list_of_survey_choices() and inputs
    the first result choice id to function get_choice_name_and_spaces(),
    then tests that the fetched choice names match
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    _, name, spaces = scs.get_choice_name_and_spaces(choices[0][0])
    assert choices[0][2] == name


def test_get_choice_additional_infos_returns_correct_data(setup_env):
    """
    Fetches all choices with get_list_of_survey_choices() and inputs
    the first result choice id to function get_choice_additional_info(),
    then tests that the fetched additional info is correct
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    choice_infos = scs.get_choice_additional_infos(choices[0][0])
    # headers
    assert choice_infos[0][0] + " " + choice_infos[1][0] == "Osoite Postinumero"
    # info
    assert choice_infos[0][1] + " " + choice_infos[1][1] == "Keijukaistenpolku 14 00820"


def test_count_number_of_available_spaces(setup_env):
    """
    Tests that function count_number_of_available_spaces returns the
    correct number
    """
    d = setup_env
    assert scs.count_number_of_available_spaces(d["survey_id"]) == 14


def test_add_empty_survey_choice(setup_env):
    """
    Tests that function add_empty_survey_choice() adds an empty choice
    with the name "Tyhjä" and the number of seats given when the
    function was called
    """
    d = setup_env
    scs.add_empty_survey_choice(d["survey_id"], 3)
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    assert choices[2].name == "Tyhjä"
    assert choices[2].max_spaces == 3


def test_check_min_equals_max(setup_env):
    """
    Tests that function check_min_equal_max() returns false
    when min_size and max_size are not equal for all of the choice
    """
    d = setup_env
    assert scs.check_min_equals_max(d["survey_id"]) == (False, 0)


def test_get_survey_choice_mandatory(setup_env):
    """
    Tests that function survey_choice_mandatory_field() returns true when the
    choice is mandatory
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    result = scs.get_survey_choice_mandatory(choices[1][0])
    assert result is True


def test_get_survey_choice_mandatory_returns_false_when_group_is_not_mandatory(setup_env):
    """
    Tests that function survey_choice_mandatory_field() returns false
    when group is not mandatory
    """
    d = setup_env
    choices = scs.get_list_of_survey_choices(d["survey_id"])
    assert scs.get_survey_choice_mandatory(choices[0][0]) is False


def test_check_answers_less_than_min_size(setup_env):
    """
    Tests that function check_answers_less_than_min_size() returns true if
    the number of answers is less than the min size of the group with the smallest min size
    """
    d = setup_env
    assert scs.check_answers_less_than_min_size(d["survey_id"], 0) is True


def test_check_answers_less_than_min_size_returns_false_if_answers_greater_than_min_size(setup_env):
    """
    Tests that function check_answers_less_than_min_size() returns false if
    the number of answers is greater than the min size of the group with the smallest min size
    """
    d = setup_env
    assert scs.check_answers_less_than_min_size(d["survey_id"], 5) is False
