from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_owners_repository import survey_owners_repository as sor


def test_add_owner_to_survey(setup_db):
    """
    Test that adding an owner to a survey works. Also test if owner added to survey
    """
    d = setup_db
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    success_add = sor.add_owner_to_survey(survey_id, d["user_id"])
    assert success_add is True
    owner = sor.check_if_owner_in_survey(survey_id, d["user_id"])
    assert owner == True


def test_add_owner_invalid_survey(setup_db):
    """
    Test that you cannot add a owner to an invalid survey
    """
    d = setup_db
    success_add = sor.add_owner_to_survey("ITSNOTREAL", d["user_id"])
    assert success_add is False


def test_get_owner_invalid_survey():
    """
    Test that you cannot get an invalid owner from an invalid survey
    """
    success_get = sor.check_if_owner_in_survey("ITSNOTREAL", -1)
    assert success_get is False


def test_exceptions(setup_db):
    """
    Test that exceptions return False
    """
    d = setup_db
    success = sor.add_owner_to_survey(-1, d["user_id"])
    assert not success
    success = sor.check_if_owner_in_survey(-1, d["user_id"])
    assert not success
