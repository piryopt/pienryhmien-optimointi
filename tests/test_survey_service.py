import pytest
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.services.survey_owners_service import survey_owners_service as sos
import datetime
import json


@pytest.fixture()
def setup_env(setup_db):
    user = ur.get_user_data(setup_db["user_id"])

    edit_dict = {
        "surveyGroupname": "Safest (most dangerous lmao) PED's",
        "surveyInformation": "No way in hell will these have long term affects on your body, mind and soul.",
        "enddate": "31.12.2077",
        "endtime": "00:00",
    }
    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    setup_db["user_email"] = user.email
    setup_db["edit_dict"] = edit_dict
    setup_db["json_object"] = json_object

    return setup_db


def test_get_survey_nonexisting_id():
    """
    Test that get_survey_returns False for an invalid survey id
    """
    assert ss.get_survey("FALSEID") is False


def test_get_survey_name_nonexisting_id():
    """
    Test that no survey name is returned for an invalid survey id
    """
    name = ss.get_survey_name("ITSNOTREAL")
    assert name is False


def test_survey_creation_case_normal(setup_env):
    """
    Tests that dict is parsed correctly to survey, its choices and their additional infos
    CASE NORMAL, the dict is valid etc.
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"],
        d["json_object"]["surveyGroupname"],
        d["user_id"],
        d["json_object"]["surveyInformation"],
        1,
        "01.01.2024",
        "02:02",
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    # check surveys tables information
    survey_name = ss.get_survey_name(survey_id)
    survey_desc = ss.get_survey_description(survey_id)
    assert survey_name == "Testikysely JSON"
    assert survey_desc == "Tällä testataan kyselyn manuaalista luomista"

    # check choice mandatory informations
    choices = scs.get_list_of_survey_choices(survey_id)
    assert choices[0][2] == "Esimerkkipäiväkoti 1"
    assert choices[0][3] == 8
    assert choices[1][2] == "Esimerkkipäiväkoti 2"
    assert choices[1][3] == 6

    choice1_infos = scs.get_choice_additional_infos(choices[0][0])
    choice2_infos = scs.get_choice_additional_infos(choices[1][0])
    assert choice1_infos[0][0] == "Osoite"
    assert choice1_infos[0][1] == "Keijukaistenpolku 14"
    assert choice1_infos[1][0] == "Postinumero"
    assert choice1_infos[1][1] == "00820"

    assert choice2_infos[0][0] == "Osoite"
    assert choice2_infos[0][1] == "Hattulantie 2"
    assert choice2_infos[1][0] == "Postinumero"
    assert choice2_infos[1][1] == "00550"


def test_count_surveys_created(setup_env):
    """
    Test survey service function count_surveys_created()
    UPDATE WHEN SURVEYS OF SAME NAME NO LONGER ACCEPTED
    """
    d = setup_env
    count = ss.count_surveys_created(d["user_id"])
    assert count == 0

    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 1", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    count = ss.count_surveys_created(d["user_id"])
    assert count == 1


def test_survey_closed(setup_env):
    """
    Test survey service functions close_survey() and check_if_survey_closed() normal cases
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 2", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    closed = ss.check_if_survey_closed(survey_id)
    assert closed is False

    ss.close_survey(survey_id, d["user_id"])
    closed = ss.check_if_survey_closed(survey_id)
    assert closed is True


def test_close_non_existing_survey(setup_env):
    """
    Test survey service functions close_survey() and check_if_survey_closed() non existing cases
    doesn't differentiate between non-existing and closed, might be a problem
    """
    d = setup_env
    ret = ss.close_survey("ITSNOTREAL", d["user_id"])
    assert ret is False

    ret = ss.check_if_survey_closed("ITSNOTREAL")
    assert ret is False


def test_wrong_owner_cant_close_survey(setup_env):
    """
    Test that wrong user id can't close an survey
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 3", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    ret = ss.close_survey(survey_id, d["user_id2"])
    assert ret is False


def test_get_list_closed_surveys(setup_env):
    """
    Test only closed surveys are acquired
    """
    d = setup_env
    closed_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 4", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(closed_id, d["user_email"])
    open_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 5", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(open_id, d["user_email"])

    ss.close_survey(closed_id, d["user_id"])

    surveys = ss.get_list_closed_surveys(d["user_id"])

    assert surveys[0][0] == closed_id
    assert len(surveys) == 1


def test_get_list_open_surveys(setup_env):
    """
    Test only open surveys are acquired
    """
    d = setup_env
    surveys = ss.get_active_surveys(d["user_id"])
    assert surveys == []
    closed_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 6", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(closed_id, d["user_email"])
    open_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 7", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(open_id, d["user_email"])

    ss.close_survey(closed_id, d["user_id"])

    surveys = ss.get_active_surveys(d["user_id"])

    assert surveys[0][0] == open_id
    assert len(surveys) == 1


def test_open_survey_normal(setup_env):
    """
    Test reopening a closed survey
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 8", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    ss.close_survey(survey_id, d["user_id"])
    closed = ss.check_if_survey_closed(survey_id)
    assert closed is True

    ss.open_survey(survey_id, d["user_id"])
    closed = ss.check_if_survey_closed(survey_id)
    assert closed is False


def test_open_survey_non_existant(setup_env):
    """
    Test opening a non-existent survey
    """
    d = setup_env
    ret = ss.open_survey("ITSNOTREAL", d["user_id"])
    assert ret is False


def test_open_survey_wrong_owner(setup_env):
    """
    Test that wrong user id can't reopen a survey
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 9", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    ss.close_survey(survey_id, d["user_id"])
    ret = ss.open_survey(survey_id, d["user_id2"])
    assert ret is False

    ret = ss.check_if_survey_closed(survey_id)
    assert ret is True


def test_check_if_survey_results_saved(setup_env):
    """
    Test functions update_survey_answered() and check_if_survey_results_saved()
    """
    d = setup_env
    ret = ss.check_if_survey_results_saved("ITSNOTREAL")
    assert ret is False
    ret = ss.update_survey_answered("ITSNOTREAL")
    assert ret is False

    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 10", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    answered = ss.check_if_survey_results_saved(survey_id)
    assert answered is False

    ss.update_survey_answered(survey_id)

    answered = ss.check_if_survey_results_saved(survey_id)
    assert answered is True


def test_get_survey_as_dict(setup_env):
    """
    Tests that survey service parser dict correctly
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 11", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    survey_dict = ss.get_survey_as_dict(survey_id)

    assert survey_dict["id"] == survey_id
    assert survey_dict["surveyname"] == "Test survey 11"
    assert survey_dict["min_choices"] == 2
    assert survey_dict["closed"] is False
    assert survey_dict["results_saved"] is False
    assert survey_dict["survey_description"] == d["json_object"]["surveyInformation"]
    assert survey_dict["time_end"] == datetime.datetime(2024, 1, 1, 2, 2)

    assert survey_dict["choices"][0]["name"] == "Esimerkkipäiväkoti 1"
    assert survey_dict["choices"][0]["max_spaces"] == 8
    assert survey_dict["choices"][0]["Osoite"] == "Keijukaistenpolku 14"
    assert survey_dict["choices"][0]["Postinumero"] == "00820"

    assert survey_dict["choices"][1]["name"] == "Esimerkkipäiväkoti 2"
    assert survey_dict["choices"][1]["max_spaces"] == 6
    assert survey_dict["choices"][1]["Osoite"] == "Hattulantie 2"
    assert survey_dict["choices"][1]["Postinumero"] == "00550"


def test_get_list_active_answered_invalid():
    """
    Test get_list_active_answered with invalid survey id
    """
    active_list = ss.get_list_active_answered("ITSNOTREAL")
    assert active_list == []


def test_get_list_closed_answered_invalid():
    """
    Test get_list_closed_answered with invalid survey id
    """
    closed_list = ss.get_list_closed_answered("ITSNOTREAL")
    assert closed_list == []


def test_get_list_active_answered(setup_env):
    """
    Test get_list_active_answered returns correct list
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 12", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking, "", "")
    active_list = ss.get_list_active_answered(d["user_id3"])
    assert len(active_list) == 1


def test_get_list_closed_answered(setup_env):
    """
    Test get_list_closed_answered returns correct list
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 12", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking, "", "")
    ss.close_survey(survey_id, d["user_id"])
    closed_list = ss.get_list_closed_answered(d["user_id3"])
    assert len(closed_list) == 1


def test_check_surveys_to_close_empty(setup_env):
    """
    Test that the function works when no open surveys
    """
    surveys = ss.check_for_surveys_to_close()
    assert surveys is False


def test_check_surveys_to_close(setup_env):
    """
    Test check_for_surveys_to_close closes surveys with past end date
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 13", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    survey_id2 = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 14", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.1999", "02:02"
    )
    sos.add_owner_to_survey(survey_id2, d["user_email"])
    surveys = ss.check_for_surveys_to_close()
    closed = ss.check_if_survey_closed(survey_id2)
    assert closed is True


def test_validate_created_survey_invalid_name(setup_env):
    """
    Test that creating a survey with a  name that is too short returns False
    """
    survey_dict = {
        "surveyGroupname": "Test",
        "surveyInformation": "Test survey validation with a name that is too short",
        "enddate": "31.12.2077",
        "endtime": "00:00",
    }

    assert ss.validate_created_survey(survey_dict) == {
        "success": False,
        "message": {"status": "0", "msg": "Kyselyn nimen tulee olla vähintään 5 merkkiä pitkä"},
    }


def test_validate_created_survey(setup_env):
    """
    Test that creating a survey with valid inputs returns True
    """

    survey_dict = {
        "surveyGroupname": "Test survey invalid min choices",
        "surveyInformation": "Test survey validation with min_choices less than 1",
        "enddate": "31.12.2077",
        "endtime": "00:00",
        "minchoices": 1,
    }

    assert ss.validate_created_survey(survey_dict) == {"success": True}


def test_validate_created_survey_invalid_min_choices(setup_env):
    """
    Test that creating a survey with min_choices that is not an integer returns False
    """
    survey_dict = {
        "surveyGroupname": "Test survey invalid min choices",
        "surveyInformation": "Test survey validation with min_choices less than 1",
        "enddate": "31.12.2077",
        "endtime": "00:00",
        "minchoices": 2.4,
    }

    survey_dict2 = {
        "surveyGroupname": "Test survey invalid min choices",
        "surveyInformation": "Test survey validation with min_choices less than 1",
        "enddate": "31.12.2077",
        "endtime": "00:00",
        "minchoices": "not a number",
    }

    assert ss.validate_created_survey(survey_dict) == {
        "success": False,
        "message": {"status": "0", "msg": "Priorisoitavien ryhmien vähimmäismäärän tulee olla numero!"},
    }

    assert ss.validate_created_survey(survey_dict2) == {
        "success": False,
        "message": {"status": "0", "msg": "Priorisoitavien ryhmien vähimmäismäärän tulee olla numero!"},
    }


def test_save_survey_edit(setup_env):
    """
    Test that editing a survey works
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 15", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    ss.save_survey_edit(survey_id, d["edit_dict"], d["user_id"])
    name = ss.get_survey_name(survey_id)
    assert name == "Safest (most dangerous lmao) PED's"
    desc = ss.get_survey_description(survey_id)
    assert desc == "No way in hell will these have long term affects on your body, mind and soul."


def test_survey_deleted(setup_env):
    """
    Test that after setting surveys as deleted it won't show up on list of active surveys
    """
    d = setup_env
    json_object = d["json_object"]
    survey_id1 = ss.create_new_survey_manual(
        json_object["choices"], "Test survey 1", d["user_id"], json_object["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    survey_id2 = ss.create_new_survey_manual(
        json_object["choices"], "Test survey 2", d["user_id"], json_object["surveyInformation"], 1, "01.01.2024", "02:02"
    )

    surveys = ss.get_all_active_surveys()
    assert len(surveys) == 2

    ss.set_survey_deleted_true(survey_id1)
    surveys = ss.get_all_active_surveys()
    assert len(surveys) == 1


def test_deleting_closed_survey_decreases_created_surveys_count(setup_env):
    """
    Test that after creating, closing, and deleting a survey,
    count_surveys_created returns 0.
    """
    d = setup_env
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey delete closed", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    count_before_deletion = ss.count_surveys_created(d["user_id"])
    assert count_before_deletion == 1
    ss.close_survey(survey_id, d["user_id"])
    ss.set_survey_deleted_true(survey_id)
    count_after_deletion = ss.count_surveys_created(d["user_id"])
    assert count_after_deletion == 0


def test_len_active_surveys(setup_env):
    """
    Test that the length of all active surveys is correct
    """
    d = setup_env
    surveys = ss.get_all_active_surveys()
    length = ss.len_all_surveys()
    assert length == 0
    assert not surveys

    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 16", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    surveys = ss.get_all_active_surveys()
    length = ss.len_all_surveys()
    assert len(surveys) == length


def test_get_correct_active_surveys_and_response_count(setup_env):
    """
    Test that service returns correct active surveys and response count to surveys that user owns
    """
    d = setup_env
    surveys = ss.get_active_surveys_and_response_count(d["user_id"])

    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 16", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )

    sos.add_owner_to_survey(survey_id, d["user_email"])

    surveys = ss.get_active_surveys_and_response_count(d["user_id"])
    assert surveys[0].surveyname == "Test survey 16"
    assert surveys[0].response_count == 0

    ranking3 = "2,1,5,6,3,4"
    ranking2 = "1,2,5,6,4,3"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking3, "", "")
    urr.add_user_ranking(d["user_id2"], survey_id, ranking2, "", "")

    surveys = ss.get_active_surveys_and_response_count(d["user_id"])
    assert surveys[0].surveyname == "Test survey 16"
    assert surveys[0].response_count == 2


def test_len_active_surveys_admin(setup_env):
    """
    Test that the length of all active surveys is correct for admin page
    """
    d = setup_env
    length = ss.len_active_surveys()
    assert length == 0

    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 17", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    length = ss.len_active_surveys()
    assert length == 1
