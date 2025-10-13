import pytest
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.repositories.survey_owners_repository import survey_owners_repository as sor


@pytest.fixture
def setup_env(setup_db):
    """
    Pytest fixture to set up survey and ranking for user rankings repository tests.
    """

    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    sor.add_owner_to_survey(survey_id, setup_db["user_id"])

    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(setup_db["user_id"], survey_id, ranking, "", "")

    setup_db["survey_id"] = survey_id
    setup_db["ranking"] = ranking

    return setup_db


def test_add_user_ranking_returns_false_if_user_id_not_correct(setup_env):
    """
    Tests that add_user_ranking() returns false if adding ranking fails
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    ranking = setup_env["ranking"]
    success = urr.add_user_ranking(user_id + 12, survey_id, ranking, "", "")
    assert success is False


def test_get_user_ranking(setup_env):
    """
    Test that getting a user ranking from the database works
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    ranking = setup_env["ranking"]
    db_ranking = urr.get_user_ranking(user_id, survey_id).ranking
    assert db_ranking == ranking


def test_get_invalid_user_ranking(setup_env):
    """
    Test that getting an invalid user ranking from the database works correctly
    """
    user_id = setup_env["user_id"]
    exists = urr.get_user_ranking(user_id, -1)
    assert exists is None


def test_delete_user_ranking(setup_env):
    """
    Test that deleting a user ranking works
    """
    user_id = setup_env["user_id"]
    survey_id = setup_env["survey_id"]
    urr.delete_user_ranking(user_id, survey_id)
    user_ranking = urr.get_user_ranking(user_id, survey_id)
    assert user_ranking is None


def test_user_ranking_rejections(setup_env):
    """
    Test that rejections are correctly placed into the database, when a ranking contains them
    """
    user_id2 = setup_env["user_id2"]
    survey_id = setup_env["survey_id"]
    ranking = "2,3,5,4,1,6"
    rejections = "9,8"
    reason = "Because seven ate nine"
    urr.add_user_ranking(user_id2, survey_id, ranking, rejections, reason)
    db_rejections = urr.get_user_ranking(user_id2, survey_id).rejections
    assert db_rejections == rejections


def test_exceptions(setup_env):
    """
    Test that exceptions return False
    """
    user_id = setup_env["user_id"]
    success = urr.delete_user_ranking(user_id, -1)
    assert not success
