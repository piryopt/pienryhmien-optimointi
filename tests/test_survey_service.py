import pytest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.services.survey_owners_service import survey_owners_service as sos
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime
import json


@pytest.fixture(autouse=True)
def test_setup_teardown():
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

    # Setup users
    user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
    user2 = User("Not on anabolic", "anabolic@tester.com", True)
    user3 = User("trt enjoyer", "ttrt@tester.com", True)
    ur.register(user1)
    ur.register(user2)
    ur.register(user3)
    user_id = ur.find_by_email(user1.email)[0]
    user_id2 = ur.find_by_email(user2.email)[0]
    user_id3 = ur.find_by_email(user3.email)[0]
    user_email = user1.email

    edit_dict = {
        "surveyGroupname": "Safest (most dangerous lmao) PED's",
        "surveyInformation": "No way in hell will these have long term affects on your body, mind and soul.",
        "enddate": "31.12.2077",
        "endtime": "00:00",
    }
    with open("tests/test_files/test_survey1.json", "r") as openfile:
        json_object = json.load(openfile)

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "user_id2": user_id2,
        "user_id3": user_id3,
        "user_email": user_email,
        "edit_dict": edit_dict,
        "json_object": json_object,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()

def test_get_survey_name_nonexisting_id():
    """
    Test that no survey name is returned for an invalid survey id
    """
    name = ss.get_survey_name("ITSNOTREAL")
    assert name is False

def test_survey_creation_case_normal(test_setup_teardown):
    """
    Tests that dict is parsed correctly to survey, its choices and their additional infos
    CASE NORMAL, the dict is valid etc.
    """
    d = test_setup_teardown
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

def test_count_surveys_created(test_setup_teardown):
    """
    Test survey service function count_surveys_created()
    UPDATE WHEN SURVEYS OF SAME NAME NO LONGER ACCEPTED
    """
    d = test_setup_teardown
    count = ss.count_surveys_created(d["user_id"])
    assert count == 0

    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 1", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    count = ss.count_surveys_created(d["user_id"])
    assert count == 1

def test_survey_closed(test_setup_teardown):
    """
    Test survey service functions close_survey() and check_if_survey_closed() normal cases
    """
    d = test_setup_teardown
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 2", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    closed = ss.check_if_survey_closed(survey_id)
    assert closed is False

    ss.close_survey(survey_id, d["user_id"])
    closed = ss.check_if_survey_closed(survey_id)
    assert closed is True

def test_close_non_existing_survey(test_setup_teardown):
    """
    Test survey service functions close_survey() and check_if_survey_closed() non existing cases
    doesn't differentiate between non-existing and closed, might be a problem
    """
    d = test_setup_teardown
    ret = ss.close_survey("ITSNOTREAL", d["user_id"])
    assert ret is False

    ret = ss.check_if_survey_closed("ITSNOTREAL")
    assert ret is False

def test_wrong_owner_cant_close_survey(test_setup_teardown):
    """
    Test that wrong user id can't close an survey
    """
    d = test_setup_teardown
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 3", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    ret = ss.close_survey(survey_id, d["user_id2"])
    assert ret is False

def test_get_list_closed_surveys(test_setup_teardown):
    """
    Test only closed surveys are acquired
    """
    d = test_setup_teardown
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

def test_get_list_open_surveys(test_setup_teardown):
    """
    Test only open surveys are acquired
    """
    d = test_setup_teardown
    surveys = ss.get_active_surveys(d["user_id"])
    assert surveys is False
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

def test_open_survey_normal(test_setup_teardown):
    """
    Test reopening a closed survey
    """
    d = test_setup_teardown
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

def test_open_survey_non_existant(test_setup_teardown):
    """
    Test opening a non-existent survey
    """
    d = test_setup_teardown
    ret = ss.open_survey("ITSNOTREAL", d["user_id"])
    assert ret is False

def test_open_survey_wrong_owner(test_setup_teardown):
    """
    Test that wrong user id can't reopen a survey
    """
    d = test_setup_teardown
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 9", d["user_id"], d["json_object"]["surveyInformation"], 1, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])

    ss.close_survey(survey_id, d["user_id"])
    ret = ss.open_survey(survey_id, d["user_id2"])
    assert ret is False

    ret = ss.check_if_survey_closed(survey_id)
    assert ret is True

def test_check_if_survey_results_saved(test_setup_teardown):
    """
    Test functions update_survey_answered() and check_if_survey_results_saved()
    """
    d = test_setup_teardown
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

def test_get_survey_as_dict(test_setup_teardown):
    """
    Tests that survey service parser dict correctly
    """
    d = test_setup_teardown
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
    assert survey_dict["choices"][0]["seats"] == 8
    assert survey_dict["choices"][0]["Osoite"] == "Keijukaistenpolku 14"
    assert survey_dict["choices"][0]["Postinumero"] == "00820"

    assert survey_dict["choices"][1]["name"] == "Esimerkkipäiväkoti 2"
    assert survey_dict["choices"][1]["seats"] == 6
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

def test_get_list_active_answered(test_setup_teardown):
    """
    Test get_list_active_answered returns correct list
    """
    d = test_setup_teardown
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 12", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking, "", "")
    active_list = ss.get_list_active_answered(d["user_id3"])
    assert len(active_list) == 1

def test_get_list_closed_answered(test_setup_teardown):
    """
    Test get_list_closed_answered returns correct list
    """
    d = test_setup_teardown
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 12", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    sos.add_owner_to_survey(survey_id, d["user_email"])
    ranking = "2,3,5,4,1,6"
    urr.add_user_ranking(d["user_id3"], survey_id, ranking, "", "")
    ss.close_survey(survey_id, d["user_id"])
    closed_list = ss.get_list_closed_answered(d["user_id3"])
    assert len(closed_list) == 1

def test_check_surveys_to_close_empty(test_setup_teardown):
    """
    Test that the function works when no open surveys
    """
    surveys = ss.check_for_surveys_to_close()
    assert surveys is False

def test_check_surveys_to_close(test_setup_teardown):
    """
    Test check_for_surveys_to_close closes surveys with past end date
    """
    d = test_setup_teardown
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

def test_save_survey_edit(test_setup_teardown):
    """
    Test that editing a survey works
    """
    d = test_setup_teardown
    survey_id = ss.create_new_survey_manual(
        d["json_object"]["choices"], "Test survey 15", d["user_id"], d["json_object"]["surveyInformation"], 2, "01.01.2024", "02:02"
    )
    ss.save_survey_edit(survey_id, d["edit_dict"], d["user_id"])
    name = ss.get_survey_name(survey_id)
    assert name == "Safest (most dangerous lmao) PED's"
    desc = ss.get_survey_description(survey_id)
    assert desc == "No way in hell will these have long term affects on your body, mind and soul."

def test_survey_deleted(test_setup_teardown):
    """
    Test that after setting surveys as deleted it won't show up on list of active surveys
    """
    d = test_setup_teardown
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

def test_len_active_surveys(test_setup_teardown):
    """
    Test that the length of all active surveys is correct
    """
    d = test_setup_teardown
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
