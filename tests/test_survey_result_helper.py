import pytest
import json
from src.entities import survey
from src.tools import survey_result_helper as srh
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.services.user_rankings_service import user_rankings_service as urs


SURVEY3_FILE = "tests/test_files/test_survey3.json"
SURVEY4_FILE = "tests/test_files/test_survey4.json"
MULTISTAGE_FILE = "tests/test_files/test_survey5.json"


def _load_survey_json(path):
    with open(path, "r") as f:
        return json.load(f)


def _create_survey_from_file(setup_db, path):
    user = ur.get_user_data(setup_db["user_id"])
    json_object = _load_survey_json(path)
    survey_id = ss.create_new_survey_manual(
        json_object["choices"],
        json_object["surveyGroupname"],
        user.id,
        json_object.get("surveyInformation", ""),
        1,
        "01.01.2026",
        "10:00",
    )
    setup_db["survey_id"] = survey_id
    return setup_db


def _create_multistage_survey_from_file(setup_db, path):
    user = ur.get_user_data(setup_db["user_id"])
    json_object = _load_survey_json(path)
    survey_id = ss.create_new_mutistage_survey_manual(
        json_object["stages"],
        json_object["surveyGroupname"],
        user.id,
        json_object.get("surveyInformation", ""),
        "01.01.2026",
        "10:00",
        json_object["minchoices_per_stage"],
    )
    setup_db["survey_id"] = survey_id
    return setup_db


@pytest.fixture()
def setup_survey3(setup_db):
    return _create_survey_from_file(setup_db, SURVEY3_FILE)


@pytest.fixture()
def setup_survey4(setup_db):
    return _create_survey_from_file(setup_db, SURVEY4_FILE)


@pytest.fixture()
def setup_multistage_survey(setup_db):
    return _create_multistage_survey_from_file(setup_db, MULTISTAGE_FILE)


def _group_ids_by_name(survey_choices):
    return {choice["name"]: choice["id"] for choice in survey_choices}


def _assignments_by_user(output):
    return {entry[0][0]: entry[2][1] for entry in output}


def _run_hungarian_for(d, survey_choices):
    user_rankings = ss.fetch_survey_responses(d["survey_id"])
    groups_dict = srh.convert_choices_groups(survey_choices)
    students_dict = srh.convert_users_students(user_rankings)
    dropped_groups_id = []

    # students_dict_original not used
    output, unranked_and_rejected, students_dict_original = srh.run_hungarian(
        d["survey_id"], len(user_rankings), groups_dict, students_dict, dropped_groups_id
    )
    return output, unranked_and_rejected, dropped_groups_id


def test_run_hungarian_all_groups_ranked(setup_survey3):
    """
    Test  where all groups are ranked by students, but there are more seats than
    students and two groups are mandatory.
    variant 1
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Toivo"], ids["Floora"], ids["Kotikallio"], ids["Nalli"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Floora"], ids["Kotikallio"], ids["Hanna"], ids["Nalli"], ids["Toivo"]]))
    ranking3 = ",".join(map(str, [ids["Kotikallio"], ids["Hanna"], ids["Nalli"], ids["Floora"], ids["Toivo"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, "", "")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, "", "")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, "", "")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Toivo"
    assert output_dict[d["user_id2"]] == "Floora"
    assert output_dict[d["user_id3"]] == "Nalli"
    assert unranked_and_rejected == 0
    assert ids["Kotikallio"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id


def test_run_hungarian_all_groups_ranked2(setup_survey3):
    """
    Test where all groups are ranked by students, but there are more seats than
    students and two groups are mandatory.
    variant 2
    """

    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Toivo"], ids["Floora"], ids["Kotikallio"], ids["Nalli"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Toivo"], ids["Kotikallio"], ids["Nalli"], ids["Hanna"], ids["Floora"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, "", "")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, "", "")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Toivo" or output_dict[d["user_id"]] == "Toivo"
    assert output_dict[d["user_id2"]] == "Nalli" or output_dict[d["user_id2"]] == "Nalli"
    assert ids["Floora"] in dropped_groups_id
    assert ids["Kotikallio"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id
    assert unranked_and_rejected == 0


def test_run_hungarian_all_students_have_same_ranking(setup_survey3):
    """
    Test case where all students have the same ranking for all groups.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking = ",".join(map(str, [ids["Toivo"], ids["Floora"], ids["Kotikallio"], ids["Nalli"], ids["Hanna"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking, "", "")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking, "", "")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking, "", "")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)

    assert ids["Toivo"] not in dropped_groups_id
    assert ids["Nalli"] not in dropped_groups_id
    assert ids["Floora"] in dropped_groups_id
    assert ids["Kotikallio"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id
    assert unranked_and_rejected == 0


def test_run_hungarian_mandatory_group_rejected(setup_survey3):
    """
    Test case where one mandatory group is rejected by all students.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Toivo"], ids["Floora"], ids["Kotikallio"], ids["Nalli"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Kotikallio"], ids["Floora"], ids["Hanna"], ids["Nalli"]]))
    ranking3 = ",".join(map(str, [ids["Kotikallio"], ids["Nalli"], ids["Hanna"], ids["Floora"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, str(ids["Toivo"]), "Hyvä perustelu")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, str(ids["Toivo"]), "Hyvä perustelu")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, str(ids["Toivo"]), "Hyvä perustelu")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Toivo" or output_dict[d["user_id"]] == "Floora"
    assert output_dict[d["user_id2"]] == "Toivo" or output_dict[d["user_id2"]] == "Kotikallio"
    assert output_dict[d["user_id3"]] == "Nalli"
    assert unranked_and_rejected == 1
    assert ids["Kotikallio"] in dropped_groups_id or ids["Floora"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id


def test_run_hungarian_mandatory_groups_unranked(setup_survey3):
    """
    Test case where one mandatory group is unranked by all students.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Floora"], ids["Kotikallio"], ids["Nalli"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Kotikallio"], ids["Floora"], ids["Hanna"], ids["Nalli"]]))
    ranking3 = ",".join(map(str, [ids["Nalli"], ids["Hanna"], ids["Floora"], ids["Kotikallio"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, "", "")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, "", "")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, "", "")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Toivo" or output_dict[d["user_id"]] == "Floora"
    assert output_dict[d["user_id2"]] == "Toivo" or output_dict[d["user_id2"]] == "Kotikallio"
    assert output_dict[d["user_id3"]] == "Nalli"
    assert unranked_and_rejected == 1
    assert ids["Kotikallio"] in dropped_groups_id or ids["Floora"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id


def test_run_hungarian_mandatory_groups_unranked2(setup_survey3):
    """
    Test case where one mandatory group is unranked by all students.
    2. variant
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Kotikallio"], ids["Hanna"], ids["Floora"]]))
    ranking2 = ",".join(map(str, [ids["Kotikallio"], ids["Hanna"], ids["Nalli"]]))
    ranking3 = ",".join(map(str, [ids["Hanna"], ids["Kotikallio"], ids["Floora"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, "", "")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, "", "")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, "", "")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id2"]] == "Nalli"
    assert output_dict[d["user_id"]] == "Toivo" or output_dict[d["user_id3"]] == "Toivo"
    assert output_dict[d["user_id"]] == "Kotikallio" or output_dict[d["user_id3"]] == "Hanna"
    assert unranked_and_rejected == 1
    assert ids["Toivo"] not in dropped_groups_id and ids["Nalli"] not in dropped_groups_id
    assert ids["Kotikallio"] in dropped_groups_id or ids["Hanna"] in dropped_groups_id
    assert ids["Floora"] in dropped_groups_id


def test_run_hungarian_mandatory_groups_unranked_and_rejected(setup_survey3):
    """
    Test case where one mandatory group is rejected by all students and another
    mandatory group is rejected by two students but unranked by one student.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Floora"], ids["Kotikallio"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Kotikallio"], ids["Floora"], ids["Hanna"]]))
    ranking3 = ",".join(map(str, [ids["Hanna"], ids["Floora"], ids["Kotikallio"]]))

    rejections1 = ",".join(map(str, [ids["Toivo"], ids["Nalli"]]))
    rejections2 = ",".join(map(str, [ids["Toivo"], ids["Nalli"]]))
    rejections3 = ",".join(map(str, [ids["Toivo"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, rejections1, "Hyvä perustelu")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, rejections2, "Hyvä perustelu")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, rejections3, "Hyvä perustelu")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Toivo" or output_dict[d["user_id"]] == "Floora"
    assert output_dict[d["user_id2"]] == "Toivo" or output_dict[d["user_id2"]] == "Kotikallio"
    assert output_dict[d["user_id3"]] == "Nalli"
    assert unranked_and_rejected == 2
    assert ids["Kotikallio"] in dropped_groups_id or ids["Floora"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id


def test_run_hungarian_not_enough_students_to_fill_all_mandatory_groups(setup_survey3):
    """
    Test case where there are not enough students to fill all mandatory groups.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Floora"], ids["Kotikallio"], ids["Hanna"]]))
    rejections1 = ",".join(map(str, [ids["Toivo"], ids["Nalli"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, rejections1, "Hyvä perustelu")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Toivo" or output_dict[d["user_id"]] == "Floora"
    assert unranked_and_rejected == 1
    assert ids["Toivo"] in dropped_groups_id or ids["Nalli"] in dropped_groups_id
    assert ids["Floora"] in dropped_groups_id
    assert ids["Kotikallio"] in dropped_groups_id
    assert ids["Hanna"] in dropped_groups_id


def test_run_hungarian_not_enough_students_to_fill_any_mandatory_groups(setup_survey4):
    """
    Test case where there are not enough students to fill any of the mandatory groups.
    """
    d = setup_survey4
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Toivo"], ids["Nalli"]]))
    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, "", "")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)
    output_dict = _assignments_by_user(output)

    assert output_dict[d["user_id"]] == "Tyhjä"
    assert unranked_and_rejected == 1
    assert ids["Toivo"] in dropped_groups_id
    assert ids["Nalli"] in dropped_groups_id


def test_happiness_results(setup_survey3):
    """
    Test happiness results calculation.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Toivo"], ids["Nalli"], ids["Kotikallio"], ids["Floora"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Hanna"], ids["Toivo"], ids["Nalli"], ids["Kotikallio"], ids["Floora"]]))
    ranking3 = ",".join(map(str, [ids["Kotikallio"], ids["Nalli"], ids["Toivo"], ids["Floora"], ids["Hanna"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, "", "")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, "", "")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, "", "")

    user_rankings = ss.fetch_survey_responses(d["survey_id"])
    groups_dict = srh.convert_choices_groups(survey_choices)
    students_dict = srh.convert_users_students(user_rankings)

    output = srh.hungarian_results(d["survey_id"], user_rankings, groups_dict, students_dict, survey_choices)
    happiness_avg = output[1]
    happiness_results_list = output[2]

    assert happiness_avg == 1.3333333333333333
    assert happiness_results_list == [(1, ". valintaansa sijoitetut käyttäjät: ", 2), (2, ". valintaansa sijoitetut käyttäjät: ", 1)]


def test_happiness_results_students_in_unranked_or_rejected(setup_survey3):
    """
    Test happiness results calculation where some students are placed in unranked
    or rejected groups.
    """
    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    d = setup_survey3
    survey_choices = scs.get_list_of_survey_choices(d["survey_id"])
    ids = _group_ids_by_name(survey_choices)

    ranking1 = ",".join(map(str, [ids["Floora"], ids["Kotikallio"], ids["Hanna"]]))
    ranking2 = ",".join(map(str, [ids["Kotikallio"], ids["Floora"], ids["Hanna"]]))
    ranking3 = ",".join(map(str, [ids["Hanna"], ids["Floora"], ids["Kotikallio"]]))

    rejections1 = ",".join(map(str, [ids["Toivo"], ids["Nalli"]]))
    rejections2 = ",".join(map(str, [ids["Toivo"], ids["Nalli"]]))
    rejections3 = ",".join(map(str, [ids["Toivo"]]))

    urs.add_user_ranking(d["user_id"], d["survey_id"], ranking1, rejections1, "Hyvä perustelu")
    urs.add_user_ranking(d["user_id2"], d["survey_id"], ranking2, rejections2, "Hyvä perustelu")
    urs.add_user_ranking(d["user_id3"], d["survey_id"], ranking3, rejections3, "Hyvä perustelu")

    output, unranked_and_rejected, dropped_groups_id = _run_hungarian_for(d, survey_choices)

    user_rankings = ss.fetch_survey_responses(d["survey_id"])
    groups_dict = srh.convert_choices_groups(survey_choices)
    students_dict = srh.convert_users_students(user_rankings)

    output = srh.hungarian_results(d["survey_id"], user_rankings, groups_dict, students_dict, survey_choices)
    happiness_avg = output[1]
    happiness_results_list = output[2]

    assert happiness_avg == 1
    assert happiness_results_list == [
        (1, ". valintaansa sijoitetut käyttäjät: ", 1),
        ("Ei järjestettyyn", " valintaan sijoitetut käyttäjät: ", 1),
        ("Kiellettyyn", " valintaan sijoitetut käyttäjät: ", 1),
    ]


def test_multistage_creation_from_json(setup_multistage_survey):
    """
    Ensure multistage survey is created from JSON and stage choices are available.
    """
    d = setup_multistage_survey
    survey_id = d["survey_id"]

    stage1_choices = scs.get_list_of_stage_survey_choices(survey_id, "Vaihe 1")
    stage2_choices = scs.get_list_of_stage_survey_choices(survey_id, "Vaihe 2")

    # Expect two choices in each stage as defined in tests/test_files/test_survey5.json
    assert isinstance(stage1_choices, list)
    assert isinstance(stage2_choices, list)
    assert len(stage1_choices) == 2
    assert len(stage2_choices) == 2

    names_stage1 = {c["name"] for c in stage1_choices}
    names_stage2 = {c["name"] for c in stage2_choices}

    assert "Päiväkoti Toivo" in names_stage1
    assert "Päiväkoti Nalli" in names_stage1
    assert "Päiväkoti Toivo" in names_stage2
    assert "Päiväkoti Nalli" in names_stage2
