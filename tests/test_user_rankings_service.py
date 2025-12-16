import pytest
from src.repositories.user_repository import user_repository as ur
from src.services.survey_service import survey_service as ss
from src.services.survey_owners_service import survey_owners_service as sos
from src.services.user_rankings_service import user_rankings_service as urs
import json


@pytest.fixture
def setup_env(setup_db):
    """
    Pytest fixture to set up survey for user rankings service tests.
    """

    user = ur.get_user_data(setup_db["user_id"])

    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    survey_id = ss.create_new_survey_manual(
        json_object["choices"], json_object["surveyGroupname"], user.id, json_object["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, user.email)

    setup_db["survey_id"] = survey_id

    return setup_db


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


def test_get_user_rejections(setup_env):
    """
    Test that a correct rejections are returned
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    success = urs.add_user_ranking(user_id, survey_id, "1,2,3,4,5,8", "6,7,9", "Because seven ate nine")
    assert success
    rejections = urs.get_user_rejections(user_id, survey_id)
    assert rejections == "6,7,9"
