from random import shuffle
from datetime import datetime
from functools import wraps
from flask import app, render_template, request, session, jsonify, redirect, Blueprint, current_app
from flask_wtf.csrf import generate_csrf
import markdown
from pathlib import Path
from flask_babel import gettext
from src import scheduler
from src.repositories.survey_repository import survey_repository
from src.services.user_service import user_service
from src.services.survey_service import survey_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.services.final_group_service import final_group_service
from src.services.survey_owners_service import survey_owners_service
from src.services.feedback_service import feedback_service
from src.tools.survey_result_helper import convert_choices_groups, convert_users_students, convert_date, convert_time, hungarian_results
from src.tools.rankings_converter import convert_to_list, convert_to_string
from src.tools.parsers import parser_csv_to_dict
from src.tools.date_converter import format_datestring
from src.entities.user import User
# from src.tools.db_data_gen import gen_data

bp = Blueprint("main", __name__)


"""
DECORATORS:
"""


def ad_login(f):
    """
    This is pretty much all the AD-login code there is.
    This function is called by some routes,
    by those marked by @home_decorator()
    For more details see documentation
    """

    @wraps(f)
    def _ad_login(*args, **kwargs):
        result = f(*args, **kwargs)
        # if logged in already do nothing or in local use
        if session.get("user_id", 0) != 0 or current_app.debug:
            return result
        roles = request.headers.get("eduPersonAffiliation", "")
        name = request.headers.get("cn", "").encode("latin-1").decode("utf-8")
        email = request.headers.get("mail", "")
        role_bool = True if "faculty" in roles or "staff" in roles else False
        email_exists = user_service.find_by_email(email)  # account doesn't exist, register
        if not email_exists:
            user_service.create_user(name, email, role_bool)  # actual registration
        logged_in = user_service.check_credentials(email)  # log in, update session etc.
        if logged_in and role_bool:
            user_service.make_user_teacher(email)
        return result

    return _ad_login


def teachers_only(f):
    """
    Decorator for verifying that the user trying to access the page is a teacher. Students get redirected to the frontpage.
    """

    @wraps(f)
    def _teachers_only(*args, **kwargs):
        # Only teachers permitted
        user_id = session.get("user_id", 0)
        if not user_service.check_if_teacher(user_id):
            return redirect("/")
        return f(*args, **kwargs)

    return _teachers_only


"""
FUNCTIONS:
"""


def check_if_owner(survey_id):
    current_user_id = session.get("user_id", 0)
    if user_service.check_if_admin(current_user_id):
        return True
    owner_true = survey_owners_service.check_if_user_is_survey_owner(survey_id, current_user_id)
    return owner_true


"""
FRONTPAGE:
"""


@bp.route("/")
@ad_login
def frontpage() -> str:
    """
    Returns the rendered skeleton template
    """
    # used in local use
    if current_app.debug and session.get("user_id", 0) == 0:
        return redirect("/auth/login")
    reloaded = session.get("reloaded", 0)
    if not reloaded:
        session["reloaded"] = True
        return redirect("/")
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return render_template("index.html")
    surveys_created = survey_service.count_surveys_created(user_id)
    active_surveys = survey_service.get_active_surveys_and_response_count(user_id)
    if not active_surveys:
        return render_template("index.html", surveys_created=surveys_created, exists=False)

    return render_template("index.html", surveys_created=surveys_created, exists=True, data=active_surveys)


"""
/SURVEYS/* ROUTES:
"""


@bp.route("/surveys/active")
@ad_login
def surveys_active():
    user_id = session.get("user_id", 0)
    active_surveys = survey_service.get_active_surveys(user_id)
    return jsonify(active_surveys)

@bp.route("/surveys/closed")
@ad_login
def surveys_closed():
    user_id = session.get("user_id", 0)
    closed_surveys = survey_service.get_list_closed_surveys(user_id)
    return jsonify(closed_surveys)

@bp.route("/surveys")
@ad_login
def previous_surveys():
    """
    For fetching previous survey list from the database
    """
    reloaded = session.get("reloaded", 0)
    if not reloaded:
        session["reloaded"] = True
        return redirect("/surveys")
    user_id = session.get("user_id", 0)
    if user_id == 0:
        return redirect("/")
    active_surveys = survey_repository.fetch_all_active_surveys(user_id)
    closed_surveys = survey_service.get_list_closed_surveys(user_id)

    return render_template("surveys.html", active_surveys=active_surveys, closed_surveys=closed_surveys)


@bp.route("/surveys/getinfo", methods=["POST"])
def get_info():
    """
    When a choice is clicked, display choice info.
    """
    choice_id = int(request.get_json())
    basic_info = survey_choices_service.get_choice_name_and_spaces(choice_id)
    additional_info = survey_choices_service.get_choice_additional_infos_not_hidden(choice_id)
    return render_template("moreinfo.html", basic=basic_info, infos=additional_info)


@bp.route("/surveys/<string:survey_id>/studentranking/<string:email>", methods=["GET"])
def expand_ranking(survey_id, email):
    """
    Return json data of user's choices and rejections
    """
    user_id = user_service.get_user_id_by_email(email)
    user_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    ranking_list = convert_to_list(user_ranking.ranking)
    rejection_list = convert_to_list(user_ranking.rejections)
    choices = []
    for r in ranking_list:
        choice = survey_choices_service.get_survey_choice(r)
        choices.append(choice)
    rejections = []
    if len(rejection_list) > 0:
        for r in rejection_list:
            choice = survey_choices_service.get_survey_choice(r)
            rejections.append(choice)
    return jsonify({"choices": choices, "rejections": rejections})


@bp.route("/surveys/create", methods=["GET"])
@ad_login
def new_survey_form(survey=None):
    """
    Page for survey creation. Adds fields automatically if user chose to copy from template

    args:
        survey: By default, none. If user copied from template, the survey is the survey from the template
    """
    query_params = request.args.to_dict()
    if "fromTemplate" in query_params:
        survey_id = query_params["fromTemplate"]
        if not check_if_owner(survey_id):
            return redirect("/")
        survey = survey_service.get_survey_as_dict(survey_id)
        survey["variable_columns"] = [
            column for column in survey["choices"][0] if (column not in {"id", "survey_id", "mandatory", "max_spaces", "deleted", "min_size", "name"})
        ]
    return render_template("create_survey.html", survey=survey)


@bp.route("/multiphase/survey/create", methods=["GET"])
@ad_login
def multiphase_survey_create():
    return render_template("create_multiphase_survey.html")


@bp.route("/surveys/create", methods=["POST"])
def new_survey_post():
    """
    Post method for creating a new survey.
    """
    data = request.get_json()
    validation = survey_service.validate_created_survey(data)
    if not validation["success"]:
        return jsonify(validation["message"])

    survey_name = data["surveyGroupname"]
    description = data["surveyInformation"]
    user_id = session.get("user_id", 0)
    survey_choices = data["choices"]
    minchoices = data["minchoices"]
    date_end = data["enddate"]
    time_end = data["endtime"]

    allowed_denied_choices = data["allowedDeniedChoices"]
    allow_search_visibility = data["allowSearchVisibility"]

    date_string = f"{date_end} {time_end}"
    format_code = "%d.%m.%Y %H:%M"

    parsed_time = datetime.strptime(date_string, format_code)

    if parsed_time <= datetime.now():
        msg = gettext("Vastausajan päättyminen ei voi olla menneisyydessä")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    if minchoices > len(survey_choices):
        msg = gettext("Vaihtoehtoja on vähemmän kuin priorisoitujen ryhmien vähimmiäismäärä! Kyselyn luominen epäonnistui!")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    survey_id = survey_service.create_new_survey_manual(
        survey_choices, survey_name, user_id, description, minchoices, date_end, time_end, allowed_denied_choices, allow_search_visibility
    )
    if not survey_id:
        msg = gettext("Tämän niminen kysely on jo käynnissä! Sulje se tai muuta nimeä!")
        response = {"status": "0", "msg": msg}
        return jsonify(response)
    email = user_service.get_email(user_id)
    (success, message) = survey_owners_service.add_owner_to_survey(survey_id, email)
    if not success:
        response = {"status": "0", "msg": message}
        return jsonify(response)
    msg = gettext("Uusi kysely luotu!")
    response = {"status": "1", "msg": msg}
    return jsonify(response)


@bp.route("/surveys/create/import", methods=["POST"])
def import_survey_choices():
    """
    Post method for creating a new survey when it uses data imported from a csv file.
    """
    data = request.get_json()
    return jsonify(parser_csv_to_dict(data["uploadedFileContent"])["choices"])


"""
/CSRF_TOKEN ROUTE:
"""


@bp.route("/csrf_token", methods=["GET"])
@ad_login
def get_csrf():
    csrf_token = generate_csrf()
    response = {"csrfToken": csrf_token}
    return jsonify(response)


"""
/SURVEYS/<SURVEY_ID>/* ROUTES:
"""


@bp.route("/surveys/<string:survey_id>")
@ad_login
def surveys(survey_id):
    """
    The answer page for surveys.
    """
    # Needed for the session bug.
    reloaded = session.get("reloaded", 0)
    if not reloaded:
        session["reloaded"] = True
        return redirect(f"/surveys/{survey_id}")

    user_id = session.get("user_id", 0)
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    survey_choices_info = survey_choices_service.survey_all_additional_infos(survey_id)
    survey = survey_service.get_survey(survey_id)

    additional_info = False
    if len(survey_choices_info) > 0:
        additional_info = True

    # If the survey has no choices, either it is an invalid survey or it doesn't exist
    if not survey_choices:
        return redirect("/")

    survey_all_info = {}
    for row in survey_choices_info:
        if row.choice_id not in survey_all_info:
            survey_all_info[row.choice_id] = {"infos": [{row.info_key: row.info_value}]}
            survey_all_info[row.choice_id]["search"] = row.info_value
        else:
            survey_all_info[row.choice_id]["infos"].append({row.info_key: row.info_value})
            survey_all_info[row.choice_id]["search"] += " " + row.info_value

    for row in survey_choices:
        if row.id not in survey_all_info:
            survey_all_info[row.id] = {"name": row.name}
            survey_all_info[row.id]["slots"] = row.max_spaces
            survey_all_info[row.id]["id"] = row.id
            survey_all_info[row.id]["mandatory"] = row.mandatory
            survey_all_info[row.id]["search"] = row.name
            survey_all_info[row.id]["infos"] = []
            survey_all_info[row.id]["min_size"] = row.min_size
        else:
            survey_all_info[row.id]["name"] = row.name
            survey_all_info[row.id]["mandatory"] = row.mandatory
            survey_all_info[row.id]["slots"] = row.max_spaces
            survey_all_info[row.id]["id"] = row.id
            survey_all_info[row.id]["min_size"] = row.min_size

    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    if user_survey_ranking:
        return surveys_answer_exists(survey_id, survey_all_info, additional_info)

    # If the survey is closed, return a different page, where the student can view their answers.
    closed = survey_service.check_if_survey_closed(survey_id)
    if closed:
        return render_template("closedsurvey.html", survey_name=survey.surveyname)

    # Shuffle the choices, so that the choices aren't displayed in a fixed order.
    shuffled_choices = list(survey_all_info.values())
    shuffle(shuffled_choices)
    return render_template("survey.html", choices=shuffled_choices, survey=survey, additional_info=additional_info)


@bp.route("/api/surveys/<string:survey_id>", methods=["GET"])
def api_survey(survey_id):
    """
    API endpoint for fetching survey data
    """
    user_id = session.get("user_id", 0)
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    survey_choices_info = survey_choices_service.survey_all_additional_infos(survey_id)
    survey = survey_service.get_survey(survey_id)

    additional_info = False
    if len(survey_choices_info) > 0:
        additional_info = True

    if not survey_choices:
        return jsonify({"error": "Survey not found"}), 404

    survey_all_info = {}
    for row in survey_choices_info:
        choice_id = str(row.choice_id)
        if choice_id not in survey_all_info:
            survey_all_info[choice_id] = {"infos": [{row.info_key: row.info_value}]}
            survey_all_info[choice_id]["search"] = row.info_value
        else:
            survey_all_info[choice_id]["infos"].append({row.info_key: row.info_value})
            survey_all_info[choice_id]["search"] += " " + row.info_value

    for row in survey_choices:
        choice_id = str(row.id)
        if choice_id not in survey_all_info:
            survey_all_info[choice_id] = {
                "name": row.name,
                "slots": row.max_spaces,
                "id": choice_id,
                "mandatory": row.mandatory,
                "search": row.name,
                "infos": [],
                "min_size": row.min_size,
            }
        else:
            survey_all_info[choice_id].update(
                {
                    "name": row.name,
                    "mandatory": row.mandatory,
                    "slots": row.max_spaces,
                    "id": choice_id,
                    "min_size": row.min_size,
                }
            )

    choices = list(survey_all_info.values())

    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    if user_survey_ranking:
        user_rankings = user_survey_ranking.ranking
        rejections = user_survey_ranking.rejections
        reason = user_survey_ranking.reason

        return jsonify(
            {
                "survey": {
                    "id": str(survey.id),
                    "name": survey.surveyname,
                    "deadline": format_datestring(survey.time_end),
                    "description": survey.survey_description,
                    "min_choices": survey.min_choices,
                    "search_visibility": survey.allow_search_visibility,
                    "denied_allowed_choices": survey.allowed_denied_choices,
                },
                "additional_info": additional_info,
                "choices": choices,
                "existing": "1",
                "goodChoices": convert_to_list(user_rankings),
                "badChoices": convert_to_list(rejections),
                "reason": reason,
            }
        )

    shuffle(choices)

    return jsonify(
        {
            "survey": {
                "id": str(survey.id),
                "name": survey.surveyname,
                "deadline": format_datestring(survey.time_end),
                "description": survey.survey_description,
                "min_choices": survey.min_choices,
                "search_visibility": survey.allow_search_visibility,
                "denied_allowed_choices": survey.allowed_denied_choices,
            },
            "additional_info": additional_info,
            "choices": choices,
            "existing": "0",
        }
    )


@bp.route("/api/surveys/<string:survey_id>", methods=["POST"])
def api_survey_submit(survey_id):
    """
    API endpoint for submitting survey answers
    """
    raw_data = request.get_json()

    bad_ids = raw_data["badIDs"]
    good_ids = raw_data["goodIDs"]

    reason = raw_data["reasons"]

    min_choices = int(raw_data["minChoices"])
    allowed_denied_choices = int(raw_data["maxBadChoices"])

    if len(good_ids) < min_choices:
        msg = gettext("Tallennus epäonnistui. Valitse vähintään ")
        response = {"status": "0", "msg": msg + str(min_choices)}
        return jsonify(response)

    if len(bad_ids) > allowed_denied_choices:
        msg = gettext("Tallennus epäonnistui. Voit hylätä enintään ")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    ranking = convert_to_string(good_ids)
    rejections = convert_to_string(bad_ids)

    # Verify that if user has rejections, they have also added a reasoning for them.
    if len(bad_ids) == 0 and len(reason) > 0:
        msg = gettext("Ei hyväksytä perusteluita, jos ei ole hylkäyksiä! Tallennus epäonnistui.")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    # Verify that the reasoning isn't too long or short.
    if len(reason) > 300:
        msg = gettext(
            "Perustelu on liian pitkä, tallenus epäonnistui. Merkkejä saa olla korkeintaan 300. Tarvittaessa ota yhteys kyselyn järjestäjään."
        )
        response = {"status": "0", "msg": msg}
        return jsonify(response)
    if len(reason) < 10 and len(bad_ids) > 0:
        msg = gettext("Perustelu on liian lyhyt, tallennus epäonnistui. Merkkeja tulee olla vähintään 10.")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    user_id = session.get("user_id", 0)
    submission = user_rankings_service.add_user_ranking(user_id, survey_id, ranking, rejections, reason)
    msg = gettext("Tallennus onnistui.")
    response = {"status": "1", "msg": msg}
    if not submission:
        msg = gettext("Tallennus epäonnistui")
        response = {"status": "0", "msg": msg}
    return jsonify(response)


@bp.route("/surveys/<string:survey_id>/answered")
def surveys_answer_exists(survey_id, survey_all_info, additional_info):
    """
    The answer page for surveys if an answer exists.
    """
    user_id = session.get("user_id", 0)
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    survey = survey_service.get_survey(survey_id)

    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    existing = "1"
    user_rankings = user_survey_ranking.ranking
    rejections = user_survey_ranking.rejections
    reason = user_survey_ranking.reason

    list_of_good_survey_choice_id = convert_to_list(user_rankings)

    good_survey_choices = []
    for survey_choice_id in list_of_good_survey_choice_id:
        survey_choice = survey_choices_service.get_survey_choice(survey_choice_id)
        good_choice = {}
        good_choice["name"] = survey_choice.name
        good_choice["id"] = survey_choice.id
        good_choice["slots"] = survey_choice.max_spaces
        good_choice["mandatory"] = survey_choice.mandatory
        good_choice["search"] = survey_all_info[int(survey_choice_id)]["search"]
        good_choice["min_size"] = survey_choice.min_size
        if not survey_choice:
            continue
        good_survey_choices.append(good_choice)
        survey_choices.remove(survey_choice)

    bad_survey_choices = []
    if len(rejections) > 0:
        list_of_bad_survey_choice_id = convert_to_list(rejections)
        for survey_choice_id in list_of_bad_survey_choice_id:
            survey_choice = survey_choices_service.get_survey_choice(survey_choice_id)
            bad_choice = {}
            bad_choice["name"] = survey_choice.name
            bad_choice["id"] = survey_choice.id
            bad_choice["slots"] = survey_choice.max_spaces
            bad_choice["mandatory"] = survey_choice.mandatory
            bad_choice["search"] = survey_all_info[int(survey_choice_id)]["search"]
            bad_choice["min_size"] = survey_choice.min_size
            if not survey_choice:
                continue
            bad_survey_choices.append(bad_choice)
            survey_choices.remove(survey_choice)

    neutral_choices = []
    for survey_choice in survey_choices:
        neutral_choice = {}
        neutral_choice["name"] = survey_choice.name
        neutral_choice["id"] = survey_choice.id
        neutral_choice["slots"] = survey_choice.max_spaces
        neutral_choice["mandatory"] = survey_choice.mandatory
        neutral_choice["search"] = survey_all_info[int(survey_choice[0])]["search"]
        neutral_choice["min_size"] = survey_choice.min_size
        neutral_choices.append(neutral_choice)

    # If the survey is closed, return a different page, where the student can view their answers.
    closed = survey_service.check_if_survey_closed(survey_id)
    if closed:
        return render_template(
            "closedsurvey.html",
            bad_survey_choices=bad_survey_choices,
            good_survey_choices=good_survey_choices,
            survey_name=survey.surveyname,
            min_choices=survey.min_choices,
        )

    return render_template(
        "survey.html",
        choices=neutral_choices,
        existing=existing,
        bad_survey_choices=bad_survey_choices,
        good_survey_choices=good_survey_choices,
        reason=reason,
        survey=survey,
        additional_info=additional_info,
    )


@bp.route("/surveys/<string:survey_id>/deletesubmission", methods=["POST"])
def delete_submission(survey_id):
    """
    Delete the current ranking of the student.
    """
    msg = gettext("Poistaminen epäonnistui!")
    response = {"status": "0", "msg": msg}
    current_user_id = session.get("user_id", 0)
    if user_rankings_service.delete_ranking(survey_id, current_user_id):
        msg = gettext("Valinnat poistettu")
        response = {"status": "1", "msg": msg}
    return jsonify(response)


@bp.route("/surveys/<string:survey_id>/answers/delete", methods=["POST"])
def owner_deletes_submission(survey_id):
    """
    Survey owner can delete a single rankinging from the survey for
    e.g. if a student has dropped the course.
    """
    if not check_if_owner(survey_id):
        response = {"message": "Only owners can delete survey answers"}
        return jsonify(response), 403
    user_data = user_service.find_by_email(request.form["student_email"])
    user_id = user_data.id
    success = user_rankings_service.delete_ranking(survey_id, user_id)
    if not success:
        return jsonify({"message": "Deleting answer failed"})
    return "", 204
    
@bp.route("/surveys/<string:survey_id>/edit", methods=["GET"])
def edit_survey_form(survey_id):
    """
    Page for editing survey. Fields are filled automatically based on the original survey.
    The fields that can be edited depend on whether there are answers to the survey or not

    args:
        survey_id: id of the survey to be edited
    """
    if not check_if_owner(survey_id):
        return redirect("/")
    survey = survey_service.get_survey_as_dict(survey_id)
    survey["variable_columns"] = [
        column for column in survey["choices"][0] if (column not in {"id", "survey_id", "mandatory", "max_spaces", "deleted", "min_size", "name"})
    ]

    # Check if the survey has answers. If it has, survey choices cannot be edited.
    survey_answers = survey_service.fetch_survey_responses(survey_id)
    edit_choices = True
    if len(survey_answers) > 0:
        edit_choices = False

    # Convert datetime.datetime(year, month, day, hour, minute) to date (dd.mm.yyyy) and time (hh:mm)
    end_date_data = survey["time_end"]
    end_date = convert_date(end_date_data)
    end_time = convert_time(end_date_data)

    survey["end_time"] = end_time
    survey["end_date"] = end_date

    return render_template("edit_survey.html", survey=survey, survey_id=survey_id, edit_choices=edit_choices)


@bp.route("/surveys/<string:survey_id>/edit", methods=["POST"])
def edit_survey_post(survey_id):
    """
    Post method for saving edits to a survey.
    """
    if not check_if_owner(survey_id):
        return redirect("/")

    edit_dict = request.get_json()
    validation = survey_service.validate_created_survey(edit_dict, edited=True)
    if not validation["success"]:
        return jsonify(validation["message"]), 400

    user_id = session.get("user_id", 0)
    (success, message) = survey_service.save_survey_edit(survey_id, edit_dict, user_id)
    if not success:
        response = {"status": "0", "msg": message}
        return jsonify(response)
    response = {"status": "1", "msg": message}
    return jsonify(response)


@bp.route("/surveys/<string:survey_id>/delete")
def delete_survey(survey_id):
    if not check_if_owner(survey_id):
        return redirect("/")
    survey_service.set_survey_deleted_true(survey_id)
    return redirect("/surveys")


@bp.route("/surveys/<string:survey_id>", methods=["DELETE"])
def delete_surveys_endpoint(survey_id):
    if not check_if_owner(survey_id):
        response = {"message": "No permission to delete survey"}
        return jsonify(response), 403
    survey_service.set_survey_deleted_true(survey_id)
    return "", 204


@bp.route("/surveys/<string:survey_id>/edit/add_owner/<string:email>", methods=["POST"])
def add_owner(survey_id, email):
    if not email:
        msg = gettext("Sähköpostiosoite puuttuu!")
        response = {"status": "0", "msg": msg}
        return jsonify(response)
    if not check_if_owner(survey_id):
        return redirect("/")
    (success, message) = survey_owners_service.add_owner_to_survey(survey_id, email)
    if not success:
        response = {"status": "0", "msg": message}
        return jsonify(response)
    response = {"status": "1", "msg": message}
    return jsonify(response)


@bp.route("/surveys/<string:survey_id>/group_sizes", methods=["GET"])
def edit_group_sizes(survey_id):
    """
    Edit group sizes in a survey and display total number of spaces vs answers
    Args:
        survey_id (int): id of the survey
    """
    if not check_if_owner(survey_id):
        return redirect("/")
    survey = survey_service.get_survey_as_dict(survey_id)
    survey["variable_columns"] = [
        column for column in survey["choices"][0] if (column not in {"id", "survey_id", "mandatory", "max_spaces", "deleted", "min_size", "name"})
    ]
    (survey_answers_amount, choice_popularities) = survey_service.get_choice_popularities(survey_id)
    available_spaces = survey_choices_service.count_number_of_available_spaces(survey_id)
    return render_template(
        "group_sizes.html",
        survey_id=survey_id,
        survey=survey,
        survey_answers_amount=survey_answers_amount,
        available_spaces=available_spaces,
        popularities=choice_popularities,
    )


@bp.route("/surveys/<string:survey_id>/group_sizes", methods=["POST"])
def post_group_sizes(survey_id):
    """
    Post method for editing group sizes in the survey
    Args:
        survey_id (int): id of the survey
    """
    if not check_if_owner(survey_id):
        return redirect("/")

    data = request.get_json()

    # validation would be here
    # if not validation["success"]:
    #    return jsonify(validation["message"]), 400

    # update_survey_group_sizes works when survey_choices is a list of dictionaries
    # just like what is used in create survey
    db_response = survey_service.update_survey_group_sizes(survey_id, data["choices"])
    response = {}
    if db_response[0] is True:
        response["status"] = "1"
        response["msg"] = gettext("Tallennus onnistui. Päivitä sivu nähdäksesi tilanne.")
    else:
        response["status"] = "0"
        response["msg"] = gettext("Tallennus epäonnistui.")

    return jsonify(response)


@bp.route("/surveys/<string:survey_id>/answers", methods=["GET"])
@ad_login
def survey_answers(survey_id):
    """
    Returns json data for displaying answers of a survey
    """
    if not check_if_owner(survey_id):
        response = {"message": "Only owners can view survey answers"}
        return jsonify(response), 403
    
    survey_name = survey_service.get_survey_name(survey_id)
    survey_answers = survey_service.fetch_survey_responses(survey_id)
    choices_data = []
    for s in survey_answers:
        choices_data.append({
            "email": user_service.get_email(s.user_id),
            "ranking": s.ranking,
            "rejections": s.rejections,
            "reason": s.reason
        })

    survey_answers_amount = len(survey_answers)
    available_spaces = survey_choices_service.count_number_of_available_spaces(survey_id)
    closed = survey_service.check_if_survey_closed(survey_id)
    answers_saved = survey_service.check_if_survey_results_saved(survey_id)

    return jsonify({
        "surveyName": survey_name,
        "surveyAnswers": choices_data,
        "surveyAnswersAmount": survey_answers_amount,
        "availableSpaces": available_spaces,
        "surveyId": survey_id,
        "closed": closed,
        "answersSaved": answers_saved,
    })


@bp.route("/surveys/<string:survey_id>/results", methods=["GET", "POST"])
@ad_login
def survey_results(survey_id):
    """
    Display results of sorting students to groups.
    For the post request, the answers are saved to the database.
    """

    if not check_if_owner(survey_id):
        return jsonify({"msg": "Only survey owners can get survey results"})


    # Check that the survey is closed. If it is open, redirect to home page.
    if not survey_service.check_if_survey_closed(survey_id):
        return jsonify({"msg": "Survey must be closed for group assignment"})

    # Check if the answers are already saved to the database. This determines which operations are available to the owner.
    saved_result_exists = survey_service.check_if_survey_results_saved(survey_id)

    user_rankings = survey_service.fetch_survey_responses(survey_id)

    if not user_rankings:
        return jsonify({"msg": "Error: Survey answers not found"})

    survey_answers_amount = len(user_rankings)

    # Check that the amount of answers is greater than the smallest min_size of a group
    answers_less_than_min_size = survey_choices_service.check_answers_less_than_min_size(survey_id, survey_answers_amount)
    if answers_less_than_min_size:
        survey_choices_service.add_empty_survey_choice(survey_id, survey_answers_amount)

    # Create the dictionaries with the correct data, so that the Hungarian algorithm can generate the results.
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    groups_dict = convert_choices_groups(survey_choices)
    students_dict = convert_users_students(user_rankings)

    output_data = hungarian_results(survey_id, user_rankings, groups_dict, students_dict, survey_choices)
    if request.method == "GET":
        return jsonify({
            "surveyId": survey_id,
            "results": output_data[0],
            "happinessData": output_data[2],
            "happiness": output_data[1],
            "resultsSaved": saved_result_exists,
            "infos": output_data[4],
            "additionalInfoKeys": output_data[5],
            "droppedGroups": output_data[3],
        })

    return save_survey_results(survey_id, output_data)


@bp.route("/surveys/<string:survey_id>/results/save")
def save_survey_results(survey_id, output_data):
    if not check_if_owner(survey_id):
        return jsonify({"msg": "Only survey owners can save results"})
    # Check if results have been saved. If they have, redirect to previous_surveys page.
    saved_result_exists = survey_service.check_if_survey_results_saved(survey_id)
    if saved_result_exists:
        return jsonify({"msg": "Survey has already been saved"})

    # Update the database entry for the survey, so that result_saved = True.
    survey_answered = survey_service.update_survey_answered(survey_id)
    if not survey_answered:
        return jsonify({"msg": "Saving survey failed"})


    # Create new database entrys for final groups of the sorted students.
    for results in output_data[0]:
        user_id = results[0][0]
        choice_id = results[2][0]
        saved = final_group_service.save_result(user_id, survey_id, choice_id)
        if not saved:
            response = {"msg": f"ERROR IN SAVING {results[0][1]} RESULTS!"}
            return jsonify(response)
        return jsonify({"msg": "Survey saved"})



@bp.route("/surveys/<string:survey_id>/close", methods=["POST"])
def close_survey(survey_id):
    """
    Close survey, so that no more answers can be submitted
    """
    user_id = session.get("user_id", 0)
    closed = survey_service.close_survey(survey_id, user_id)
    if not closed:
        response = {"status": "0", "msg": "closing survey failed"}
        return jsonify(response)
    return jsonify({"status": "1", "msg": "Survey closed"})


@bp.route("/surveys/<string:survey_id>/open", methods=["POST"])
def open_survey(survey_id):
    """
    Open survey back up so that students can submit answers
    """
    user_id = session.get("user_id", 0)
    opened = survey_service.open_survey(survey_id, user_id)
    if not opened:
        response = {"status": "0", "msg": "Opening survey failed"}
        return jsonify(response)
    return jsonify({"status": "1", "msg": "Survey opened"})


"""
/AUTH/* ROUTES:
"""


@bp.route("/api/config", methods=["GET"])
def api_config():
    """
    Return to the frontend (DEBUG flag)
    """
    return jsonify({"debug": current_app.debug})


@bp.route("/api/session", methods=["GET"])
def api_session():
    """
    helper: return current session information as JSON.
    """
    user_id = session.get("user_id", 0)
    if not user_id:
        return jsonify({"logged_in": False})
    return jsonify(
        {
            "logged_in": True,
            "user_id": user_id,
            "email": session.get("email"),
            "full_name": session.get("full_name"),
            "role": session.get("role"),
            "language": session.get("language"),
            "admin": session.get("admin", False),
        }
    )


@bp.route("/auth/login", methods=["GET", "POST"])
def login():
    if not current_app.debug:
        return redirect("/")

    users = [
        User("outi1", "testi.opettaja@helsinki.fi", True),
        User("olli1", "testi.opiskelija@helsinki.fi", False),
        User("robottiStudent", "robotti.student@helsinki.fi", False),
        User("robottiTeacher", "robotti.teacher@helsinki.fi", True),
        User("robottiTeacher2", "robotti.2.teacher@helsinki.fi", True),
        User("Ääpö Wokki", "hm@helsinki.fi", True),
        User("opettaja", "opettaja@mail.com", True),
    ]

    if request.method == "GET":
        return render_template("mock_ad.html")
    if request.method == "POST":
        username = request.form.get("username")

        email = name = role_bool = ""

        for user in users:
            if user.name == username:
                email = user.email
                name = user.name
                role_bool = user.isteacher
                break

        if not email:
            return jsonify({"message": "Invalid username"}), 401
        
        if not user_service.find_by_email(email):  # account doesn't exist, register
            user_service.create_user(name, email, role_bool)  # actual registration

        if user_service.check_credentials(email):  # log in, update session etc.
            if role_bool:
                user_service.make_user_teacher(email)

        return redirect("/")


@bp.route("/auth/logout")
def logout():
    user_service.logout()

    # stupid, but Openshift getenv() can't find Openshift secrets,
    # so here we are
    if current_app.debug:
        return redirect("/")
    else:
        return redirect("/Shibboleth.sso/Logout")


@bp.route("/api/logout", methods=["POST"])
def api_logout():
    """
    SPA logout: clear server session and return JSON.
    """
    user_service.logout()
    return jsonify({"logged_out": True})


"""
ADMINTOOLS -ROUTES:
"""


@bp.route("/admintools/analytics")
def admin_analytics():
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    data = []
    all_created_surveys = survey_service.len_all_surveys()
    all_active_surveys = survey_service.len_active_surveys()
    all_students = user_service.len_all_students()
    all_student_rankings = user_rankings_service.len_all_rankings()
    all_teachers = user_service.len_all_teachers()

    data.append(all_created_surveys)
    data.append(all_active_surveys)
    data.append(all_students)
    data.append(all_student_rankings)
    data.append(all_teachers)

    return render_template("admintools/admin_analytics.html", data=data)


@bp.route("/admintools/feedback")
def admin_feedback():
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    data = feedback_service.get_unsolved_feedback()

    return render_template("admintools/admin_feedback.html", data=data)


@bp.route("/admintools/feedback/closed")
def admin_closed_feedback():
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    data = feedback_service.get_solved_feedback()

    return render_template("admintools/admin_closed_feedback.html", data=data)


@bp.route("/admintools/feedback/<int:feedback_id>")
def admin_feedback_data(feedback_id):
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    feedback = feedback_service.get_feedback(feedback_id)
    if not feedback:
        return redirect("/")
    return render_template("admintools/admin_feedback_data.html", feedback=feedback)


@bp.route("/admintools/feedback/<int:feedback_id>/close", methods=["POST"])
def admin_feedback_close_feedback(feedback_id):
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")
    success = feedback_service.mark_feedback_solved(feedback_id)
    if not success:
        return redirect("/")
    return redirect("/admintools/feedback")


"""
API ADMINTOOLS
"""


@bp.route("/api/admintools/feedback")
def api_admin_feedback_list():
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    if not user_service.check_if_admin(user_id):
        return jsonify({"success": False, "error": "unauthorized"}), 403
    
    rows = feedback_service.get_unsolved_feedback()
    items = []
    for r in rows:
        items.append({
            "id": r[0],
            "title": r[1],
            "type": r[2],
            "email": r[3]
        })
    return jsonify({"success": True, "data": items}), 200


@bp.route("/api/admintools/feedback/closed")
def api_admin_feedback_closed_list():
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    if not user_service.check_if_admin(user_id):
        return jsonify({"success": False, "error": "unauthorized"}), 403

    rows = feedback_service.get_solved_feedback()
    items = []
    for r in rows:
        items.append({
            "id": r[0],
            "title": r[1],
            "type": r[2],
            "email": r[3]
        })
    return jsonify({"success": True, "data": items}), 200


@bp.route("/api/admintools/feedback/<int:feedback_id>")
def api_admin_feedback_get(feedback_id):
    user_id = session.get("user_id", 0)
    if not user_service.check_if_admin(user_id):
        return jsonify({"success": False, "error": "unauthorized"}), 403
    
    r = feedback_service.get_feedback(feedback_id)
    if not r:
        return jsonify({"success": False, "error": "not_found"}), 404
    
    result = {
        "id": r[0],
        "title": r[1],
        "type": r[2],
        "email": r[3],
        "content": r[4],
        "solved": bool(r[5])
    }
    return jsonify({"success": True, "data": result}), 200


@bp.route("/api/admintools/feedback/<int:feedback_id>/close", methods=["POST"])
def api_admin_feedback_close(feedback_id):
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    if not user_service.check_if_admin(user_id):
        return jsonify({"success": False, "error": "unauthorized"}), 403
    
    success = feedback_service.mark_feedback_solved(feedback_id)
    if not success:
        return jsonify({"success": False, "error": "server_error"}), 500
    
    return jsonify({"success": True, "msg": "feedback_closed"}), 200


@bp.route("/admintools/surveys", methods=["GET"])
def admin_all_active_surveys():
    # Only admins permitted!
    user_id = session.get("user_id", 0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")
    data = survey_service.get_all_active_surveys()
    if not data:
        return redirect("/")
    return render_template("/admintools/admin_survey_list.html", data=data)


# @app.route("/admintools/gen_data", methods=["GET", "POST"])
# def admin_gen_data():
#    """
#    Page for generating users, a survey and user rankings. DELETE BEFORE PRODUCTION!!!
#    """
#    from scripts import fill_database_with_survey_answers
#
#    students = int(request.args.get("students"))
#    groups = int(request.args.get("groups"))
#    fill_database_with_survey_answers.fill_database(groups, students)
#    return redirect("/")
#
#
#    user_id = session.get("user_id",0)
#    surveys = survey_repository.fetch_all_active_surveys(user_id)
#    if request.method == "GET":
#        return render_template("/admintools/gen_data.html", surveys = surveys)
#
#    if request.method == "POST":
#        student_n = request.form.get("student_n")
#        gen_data.generate_users(int(student_n))
#        gen_data.add_generated_users_db()
#        return redirect("/admintools/gen_data")
#
# @bp.route("/admintools/gen_data/rankings", methods = ["POST"])
# def admin_gen_rankings():
#    """
#    Generate user rankings for a survey (chosen from a list) for testing. DELETE BEFORE PRODUCTION!!!
#    """
#    survey_id = request.form.get("survey_list")
#    gen_data.generate_rankings(survey_id)
#
#    return redirect(f"/surveys/{survey_id}/answers")

"""
MISCELLANEOUS ROUTES:
"""


@bp.route("/privacy-policy")
def privacy_policy():
    """
    Route returns the Privacy Policy -page linked in the footer
    """
    privacy_policy_file = Path(__file__).parents[0] / "static" / "content" / "Tietosuojaseloste.md"
    title = "Tietosuojaseloste"
    if session.get("language", 0) == "en":
        privacy_policy_file = Path(__file__).parents[0] / "static" / "content" / "privacypolicy-en.md"
        title = "Privacy policy"
    elif session.get("language", 0) == "sv":
        privacy_policy_file = Path(__file__).parents[0] / "static" / "content" / "privacypolicy-sv.md"
        title = "Integritets policy"
    content = open(privacy_policy_file, "r", encoding="utf-8").read()
    return render_template("content-page.html", content=markdown.markdown(content), title=title)


@bp.route("/faq")
def faq():
    """
    Route returns the Frequently Asked Questions -page linked in the footer
    """
    faq_file = Path(__file__).parents[0] / "static" / "content" / "faq-fi.md"
    title = "UKK"
    if session.get("language", 0) == "en":
        faq_file = Path(__file__).parents[0] / "static" / "content" / "faq-en.md"
        title = "FAQ"
    elif session.get("language", 0) == "sv":
        faq_file = Path(__file__).parents[0] / "static" / "content" / "faq-sv.md"
        title = "FAQ"
    content = open(faq_file, "r", encoding="utf-8").read()
    return render_template("content-page.html", content=markdown.markdown(content), title=title)


@bp.route("/csv-instructions")
def csv_instructions():
    """
    Route returns the csv instructions -page linked in the footer
    """
    csv_file = Path(__file__).parents[0] / "static" / "content" / "csv-instructions-fi.md"
    title = "CSV ohjeet"
    if session.get("language", 0) == "en":
        csv_file = Path(__file__).parents[0] / "static" / "content" / "csv-instructions-en.md"
        title = "CSV instructions"
    elif session.get("language", 0) == "sv":
        csv_file = Path(__file__).parents[0] / "static" / "content" / "csv-instructions-sv.md"
        title = "CSV guide"
    content = open(csv_file, "r", encoding="utf-8").read()
    return render_template("content-page.html", content=markdown.markdown(content), title=title)


@bp.route("/get_choices/<string:survey_id>", methods=["POST"])
def get_choices(survey_id):
    """
    Save the ranking to the database.
    """
    raw_data = request.get_json()

    # list of ids of choices not put in either of the boxes
    neutral_ids = raw_data["neutralIDs"]

    # list of ids of choices put in red box
    bad_ids = raw_data["badIDs"]

    # list of ids of choices put in green box
    good_ids = raw_data["goodIDs"]

    # list of all ids
    all_ids = raw_data["allIDs"]

    # value of textarea reasons
    reason = raw_data["reasons"]

    # minimum number of choices in the green box
    min_choices = int(raw_data["minChoices"])

    # maximum number of choices in the red box
    allowed_denied_choices = int(raw_data["maxBadChoices"])

    if len(good_ids) < min_choices:
        msg = gettext("Tallennus epäonnistui. Valitse vähintään ")
        response = {"status": "0", "msg": msg + str(min_choices)}
        return jsonify(response)

    if len(bad_ids) > allowed_denied_choices:
        msg = gettext("Tallennus epäonnistui. Voit hylätä enintään ")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    ranking = convert_to_string(good_ids)
    rejections = convert_to_string(bad_ids)

    # Verify that if user has rejections, they have also added a reasoning for them.
    if len(bad_ids) == 0 and len(reason) > 0:
        msg = gettext("Ei hyväksytä perusteluita, jos ei ole hylkäyksiä! Tallennus epäonnistui.")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    # Verify that the reasoning isn't too long or short.
    if len(reason) > 300:
        msg = gettext(
            "Perustelu on liian pitkä, tallenus epäonnistui. Merkkejä saa olla korkeintaan 300. Tarvittaessa ota yhteys kyselyn järjestäjään."
        )
        response = {"status": "0", "msg": msg}
        return jsonify(response)
    if len(reason) < 10 and len(bad_ids) > 0:
        msg = gettext("Perustelu on liian lyhyt, tallennus epäonnistui. Merkkeja tulee olla vähintään 10.")
        response = {"status": "0", "msg": msg}
        return jsonify(response)

    user_id = session.get("user_id", 0)
    submission = user_rankings_service.add_user_ranking(user_id, survey_id, ranking, rejections, reason)
    msg = gettext("Tallennus onnistui.")
    response = {"status": "1", "msg": msg}
    if not submission:
        msg = gettext("Tallennus epäonnistui")
        response = {"status": "0", "msg": msg}
    return jsonify(response)


@bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    if request.method == "GET":
        return jsonify({"success": False, "status": "0", "key": "use_react", "msg": gettext("Please use the React frontend for feedback")}), 200
    try:
        data = request.get_json(force=True)
    except Exception:
        data = {}
    user_id = session.get("user_id", 0)
    success, key, msg = feedback_service.new_feedback(user_id, data)
    status = "1" if success else "0"
    return jsonify({"success": success, "status": status, "key": key, "msg": msg})


@bp.route("/language/en")
def language_en():
    user_id = session.get("user_id", 0)
    success = user_service.update_user_language(user_id, "en")
    if success:
        response = {"status": "1", "msg": "Updated language to english!"}
        return jsonify(response)


@bp.route("/language/fi")
def language_fi():
    user_id = session.get("user_id", 0)
    success = user_service.update_user_language(user_id, "fi")
    if success:
        response = {"status": "1", "msg": "Kieli vaihdettu suomeksi!"}
        return jsonify(response)


@bp.route("/language/sv")
def language_sv():
    user_id = session.get("user_id", 0)
    success = user_service.update_user_language(user_id, "sv")
    if success:
        response = {"status": "1", "msg": "Uppdatera språket till svenska!"}
        return jsonify(response)


"""
TASKS:
"""


def close_surveys():
    """
    Every hour go through a list of a all open surveys. Close all surveys which have an end_date equal or less to now
    """
    survey_service.check_for_surveys_to_close()
