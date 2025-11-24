import pytest
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.survey_owners_repository import survey_owners_repository as so


@pytest.fixture()
def setup_env(setup_db):
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 02:02")
    so.add_owner_to_survey(survey_id, setup_db["user_id"])
    choice_id = scr.create_new_survey_choice(survey_id, "choice 1", 10, 5, False)
    choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 5, False)

    setup_db["survey_id"] = survey_id
    setup_db["choice_id"] = choice_id
    setup_db["choice_id2"] = choice_id2

    return setup_db


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


def test_get_survey_choice_returns_none_forn_nonexistant_choice(setup_env):
    """
    Test that getting a survey choice returns None if choice doesn't exist
    """
    d = setup_env
    choice = scr.get_survey_choice(d["choice_id"] + 12)
    assert choice is None


def test_create_new_survey_choice_returns_none_for_exception():
    """
    Test that a survey choice is not added if there's an error in survey id
    and that return is None
    """
    survey_choice_id = scr.create_new_survey_choice("not a survey", "choice 1", 10, 5, False)
    assert survey_choice_id is None


def test_get_invalid_choice():
    """
    Test that getting an invalid survey choice behaves the correct way
    """
    choice = scr.get_survey_choice("ITSNOTREAL")
    assert choice is None


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

def test_remove_empty_choices(setup_env):
    """
    Tests if empty choices are removed
    """
    d = setup_env
    scr.create_new_survey_choice(d["survey_id"], "Tyhjä", 2, 0, False)
    choice_list = scr.find_survey_choices(d["survey_id"])
    assert len(choice_list) == 3
    scr.remove_empty_choices(d["survey_id"])
    updated_choice_list = scr.find_survey_choices(d["survey_id"])
    assert len(updated_choice_list) == 2

def test_exceptions():
    """
    Test that exceptions return False
    """
    success = scr.find_survey_choices(-1)
    assert not success
    success = scr.get_all_additional_infos(-1)
    assert not success
    success = scr.edit_choice_group_size(-1, "", -1)
    assert not success
    success = scr.edit_choice_group_size_by_id(-1, -1)
    assert not success
    success = scr.get_choice_additional_infos(-1)
    assert not success
    success = scr.get_choice_additional_infos_not_hidden(-1)
    assert not success
    success = scr.set_choices_deleted_true(-1)
    assert not success
    success = scr.set_choices_deleted_false(-1)
    assert not success
    success = scr.get_choices_grouped_by_stage(-1)
    assert not success
    success = scr.get_stage_choices(-1, 0)
    assert not success
    success = scr.count_spaces_in_stage(-1, 0)
    assert not success
    success = scr.remove_empty_choices(-1)
    assert not success
