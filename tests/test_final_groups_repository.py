from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.final_group_repository import final_group_repository as fgr
from src.repositories.survey_owners_repository import survey_owners_repository as so


def test_save_result(setup_db):
    """
    Test that the results are saved into the database
    """
    d = setup_db
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 01:01.00")
    so.add_owner_to_survey(survey_id, d["user_id"])
    choice_id1 = scr.create_new_survey_choice(survey_id, "choice 1", 10, 1, False)
    choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 1, False)

    success = fgr.save_result(d["user_id"], survey_id, choice_id2)
    assert success is True


def test_result_not_saved_if_user_not_found(setup_db):
    d = setup_db
    survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2024-01-01 01:01.00")
    so.add_owner_to_survey(survey_id, d["user_id"])
    choice_id1 = scr.create_new_survey_choice(survey_id, "choice 1", 10, 1, False)
    choice_id2 = scr.create_new_survey_choice(survey_id, "choice 2", 10, 1, False)

    success = fgr.save_result(d["user_id"] + 12, survey_id, choice_id2)
    assert success is False
