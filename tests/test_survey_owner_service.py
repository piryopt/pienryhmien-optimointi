import pytest
from src.services.survey_service import survey_service as ss
from src.repositories.user_repository import user_repository as ur
from src.services.survey_owners_service import survey_owners_service as sos
import json


@pytest.fixture()
def setup_env(setup_db):
    user = ur.get_user_data(setup_db["user_id"])

    setup_db["user_email"] = user.email

    return setup_db


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
