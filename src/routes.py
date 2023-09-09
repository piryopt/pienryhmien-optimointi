from random import shuffle
from functools import wraps
from sqlalchemy import text
from flask import render_template, request, session, jsonify, redirect
import os
import markdown
from pathlib import Path

from src import app,db,scheduler,csrf
from src.repositories.survey_repository import survey_repository
from src.services.user_service import user_service
from src.services.survey_service import survey_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.services.final_group_service import final_group_service
from src.services.survey_teachers_service import survey_teachers_service
from src.services.feedback_service import feedback_service
from src.tools import excelreader
import src.algorithms.hungarian as h
import src.algorithms.weights as w
from src.tools.survey_result_helper import convert_choices_groups, convert_users_students, get_happiness, convert_date, convert_time
from src.tools.rankings_converter import convert_to_list, convert_to_string
from src.tools.parsers import parser_elomake_csv_to_dict
from src.entities.user import User
from functools import wraps 
from datetime import datetime

"""
DECORATORS:
"""

def ad_login(f):
    '''
    This is pretty much all the AD-login code there is.
    This function is called by some routes, 
    by those marked by @home_decorator()
    For more details see documentation
    '''
    @wraps(f)
    def _ad_login(*args, **kwargs):
        result = f(*args, **kwargs)
        # if logged in already do nothing or in local use
        if session.get("user_id", 0) != 0 or app.debug:
            return result
        roles = request.headers.get('eduPersonAffiliation')
        name = request.headers.get('cn')
        email = request.headers.get('mail')
        role_bool = True if "faculty" in roles or "staff" in roles else False
        email_exists = user_service.find_by_email(email) # account doesn't exist, register
        if not email_exists:
            user_service.create_user(name, email, role_bool) # actual registration
        logged_in = user_service.check_credentials(email) # log in, update session etc.
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
        user_id = session.get("user_id",0)
        if not user_service.check_if_teacher(user_id):
            return redirect("/")
        return f(*args, **kwargs)
    return _teachers_only

"""
FRONTPAGE:
"""
@app.route("/")
@ad_login
def frontpage() -> str:
    """
    Returns the rendered skeleton template
    """
    # used in local use
    if app.debug and session.get("user_id", 0) == 0:
        return redirect("/auth/login")
    reloaded = session.get("reloaded",0)
    if not reloaded:
        session["reloaded"] = True
        return redirect("/")
    user_id = session.get("user_id",0)
    if user_id == 0:
        return render_template('index.html')
    is_teacher = user_service.check_if_teacher(user_id)
    if not is_teacher:
         return render_template('index.html', exists = False, is_teacher = is_teacher)
    surveys_created = survey_service.count_surveys_created(user_id)
    # If 0 surveys created, return the base home page.
    if surveys_created == 0:
        return render_template('index.html', surveys_created = 0, exists = False, is_teacher = is_teacher)
    surveys = survey_service.get_active_surveys(user_id)
    if not surveys:
        return render_template('index.html', surveys_created = surveys_created, exists = False, is_teacher = is_teacher)
    data = []
    for s in surveys:
        survey_id = s[0]
        surveyname = s[1]
        survey_answers = survey_service.fetch_survey_responses(survey_id)
        participants = len(survey_answers)
        survey_ending_date = survey_service.get_survey_enddate(survey_id)
        data.append([survey_id, surveyname, participants, survey_ending_date])

    return render_template('index.html', surveys_created = surveys_created, exists = True, data = data, is_teacher = is_teacher)

"""
/SURVEYS/* ROUTES:
"""
@app.route("/surveys")
@ad_login
def previous_surveys():
    """
    For fetching previous survey list from the database
    """
    reloaded = session.get("reloaded",0)
    if not reloaded:
        session["reloaded"] = True
        return redirect("/surveys")
    user_id = session.get("user_id",0)
    if user_id == 0:
        return redirect('/')
    is_teacher = user_service.check_if_teacher(user_id)
    active_surveys = []
    closed_surveys = []
    if is_teacher:
        active_surveys = survey_repository.fetch_all_active_surveys(user_id)
        closed_surveys = survey_service.get_list_closed_surveys(user_id)
    else:
        active_surveys = survey_service.get_list_active_answered(user_id)
        closed_surveys = survey_service.get_list_closed_answered(user_id)

    return render_template("surveys.html", active_surveys=active_surveys, closed_surveys = closed_surveys, is_teacher = is_teacher)

@app.route("/surveys/getinfo", methods=["POST"])
def get_info():
    """
    When a choice is clicked, display choice info.
    """
    raw_id = request.get_json()
    basic_info = survey_choices_service.get_choice_name_and_spaces(int(raw_id))
    additional_info = survey_choices_service.get_choice_additional_infos_not_hidden(int(raw_id))
    return render_template("moreinfo.html", basic = basic_info, infos = additional_info)

@app.route("/surveys/create", methods = ["GET"])
@ad_login
@teachers_only
def new_survey_form(survey=None):
    """
    Page for survey creation. Adds fields automatically if user chose to copy from template

    args:
        survey: By default, none. If user copied from template, the survey is the survey from the template
    """
    query_params = request.args.to_dict()
    if("fromTemplate" in query_params):
        survey = survey_service.get_survey_as_dict(query_params["fromTemplate"])
        survey["variable_columns"] = [column for column in survey["choices"][0] if (column != "name" and column != "seats" and column != "id")]
    return render_template("create_survey.html", survey=survey)

@app.route("/surveys/create", methods = ["POST"])
@teachers_only
def new_survey_post():
    """
    Post method for creating a new survey.
    """
    data = request.get_json()

    validation = survey_service.validate_created_survey(data)
    if not validation["success"]:
        return jsonify(validation["message"]), 400

    survey_name = data["surveyGroupname"]
    description = data["surveyInformation"]
    user_id = session.get("user_id",0)
    survey_choices = data["choices"]
    minchoices = data["minchoices"]

    date_begin = data["startdate"]
    time_begin = data["starttime"]

    date_end = data["enddate"]
    time_end = data["endtime"]

    allowed_denied_choices = data["allowedDeniedChoices"]
    allow_search_visibility = data["allowSearchVisibility"]

    if minchoices > len(survey_choices):
        response = {"status":"0", "msg":"Vaihtoehtoja on vähemmän kuin priorisoitujen ryhmien vähimmiäismäärä! Kyselyn luominen epäonnistui!"}
        return jsonify(response)

    survey_id = survey_service.create_new_survey_manual(survey_choices, survey_name, user_id, description, minchoices, date_begin, time_begin, date_end, time_end, allowed_denied_choices, allow_search_visibility)
    if not survey_id:
        response = {"status":"0", "msg":"Tämän niminen kysely on jo käynnissä! Sulje se tai muuta nimeä!"}
        return jsonify(response)
    teacher_email = user_service.get_email(user_id)
    (success, message) = survey_teachers_service.add_teacher_to_survey(survey_id, teacher_email)
    if not success:
        response = {"status":"0", "msg":message}
        return jsonify(response)
    response = {"status":"1", "msg":"Uusi kysely luotu!"}
    return jsonify(response)

@app.route("/surveys/create/import", methods = ["POST"])
@teachers_only
def import_survey_choices():
    """
    Post method for creating a new survey when it uses data imported from a csv file.
    """
    data = request.get_json()
    return jsonify(parser_elomake_csv_to_dict(data['uploadedFileContent'])["choices"])

"""
/SURVEYS/<SURVEY_ID>/* ROUTES:
"""
@app.route("/surveys/<string:survey_id>")
@ad_login
def surveys(survey_id):
    """
    The answer page for surveys.
    """
    # Needed for the session bug. 
    reloaded = session.get("reloaded",0)
    if not reloaded:
        session["reloaded"] = True
        return redirect(f"/surveys/{survey_id}")

    user_id = session.get("user_id",0)
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    survey_choices_info = survey_choices_service.survey_all_additional_infos(survey_id)
    survey = survey_service.get_survey(survey_id)

    # If the survey has no choices, either it is an invalid survey or it doesn't exist
    if not survey_choices:
        return redirect("/")

    survey_all_info = {}
    for row in survey_choices_info:
        if row[0] not in survey_all_info:
            survey_all_info[row[0]] = {"infos": [{row[1]:row[2]}]}
            survey_all_info[row[0]]["search"] = row[2]
        else:
            survey_all_info[row[0]]["infos"].append({row[1]:row[2]})
            survey_all_info[row[0]]["search"] += " " + row[2]

    for row in survey_choices:
        if row[0] not in survey_all_info:
            survey_all_info[row[0]] = {"name": row[2]}
            survey_all_info[row[0]]["slots"] = row[3]
            survey_all_info[row[0]]["id"] = row[0]
            survey_all_info[row[0]]["search"] = row[2]
            survey_all_info[row[0]]["infos"] = []
        else:
            survey_all_info[row[0]]["name"] = row[2]
            survey_all_info[row[0]]["slots"] = row[3]
            survey_all_info[row[0]]["id"] = row[0]

    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    if user_survey_ranking:
        return surveys_answer_exists(survey_id, survey_all_info)
    
    # If the survey is closed, return a different page, where the student can view their answers.
    closed = survey_service.check_if_survey_closed(survey_id)
    if closed:
        return render_template("closedsurvey.html", survey_name = survey[1])

    # Shuffle the choices, so that the choices aren't displayed in a fixed order.
    temp = list(survey_all_info.items())
    shuffle(temp)
    shuffled_choices = [v for k,v in dict(temp).items()]

    return render_template("survey.html", choices = shuffled_choices, survey = survey)

@app.route("/surveys/<string:survey_id>/answered")
def surveys_answer_exists(survey_id, survey_all_info):
    """
    The answer page for surveys if an answer exists.
    """
    user_id = session.get("user_id",0)
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    survey = survey_service.get_survey(survey_id)

    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    existing = "1"
    user_rankings = user_survey_ranking[3]
    rejections = user_survey_ranking[4]
    reason = user_survey_ranking[5]

    list_of_good_survey_choice_id = convert_to_list(user_rankings)

    good_survey_choices = []
    for survey_choice_id in list_of_good_survey_choice_id:
        survey_choice = survey_choices_service.get_survey_choice(survey_choice_id)
        good_choice = {}
        good_choice["name"] = survey_choice[2]
        good_choice["id"] = survey_choice[0]
        good_choice["slots"] = survey_choice[3]
        good_choice["search"] = survey_all_info[int(survey_choice_id)]["search"]
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
            bad_choice["name"] = survey_choice[2]
            bad_choice["id"] = survey_choice[0]
            bad_choice["slots"] = survey_choice[3]
            bad_choice["search"] = survey_all_info[int(survey_choice_id)]["search"]
            if not survey_choice:
                continue
            bad_survey_choices.append(bad_choice)
            survey_choices.remove(survey_choice)
    
    neutral_choices = []
    for survey_choice in survey_choices:
        neutral_choice = {}
        neutral_choice["name"] = survey_choice[2]
        neutral_choice["id"] = survey_choice[0]
        neutral_choice["slots"] = survey_choice[3]
        neutral_choice["search"] = survey_all_info[int(survey_choice[0])]["search"]
        neutral_choices.append(neutral_choice)

    # If the survey is closed, return a different page, where the student can view their answers.
    closed = survey_service.check_if_survey_closed(survey_id)
    if closed:
        return render_template("closedsurvey.html", bad_survey_choices = bad_survey_choices, good_survey_choices=good_survey_choices,
                                 survey_name = survey[1], min_choices = survey[2])

    return render_template("survey.html", choices = neutral_choices, existing = existing,
                        bad_survey_choices = bad_survey_choices, good_survey_choices=good_survey_choices, reason=reason, survey = survey)

@app.route("/surveys/<string:survey_id>/deletesubmission", methods=["POST"])
def delete_submission(survey_id):
    """
    Delete the current ranking of the student.
    """
    response = {"status":"0", "msg":"Poistaminen epäonnistui"}
    current_user_id = session.get("user_id", 0)
    if user_rankings_service.delete_ranking(survey_id, current_user_id):
        response = {"status":"1", "msg":"Valinnat poistettu"}
    return jsonify(response)

@app.route("/surveys/<string:survey_id>/answers/delete", methods=["POST"])
@teachers_only
def teacher_deletes_submission(survey_id):
    '''
    Teacher (survey author) can delete a single rankinging from the survey for
    e.g. if a student has dropped the course.
    '''
    user_data = user_service.find_by_email(request.form["student_email"])
    user_id = user_data.id
    user_rankings_service.delete_ranking(survey_id, user_id)
    return redirect(f'/surveys/{survey_id}/answers')

@app.route("/surveys/<string:survey_id>/edit", methods = ["GET"])
@teachers_only
def edit_survey_form(survey_id):
    """
    Page for editing survey. Fields are filled automatically based on the original survey.
    The fields that can be edited depend on wether there are answers to the survey or not

    args:
        survey_id: id of the survey to be edited
    """

    survey = survey_service.get_survey_as_dict(survey_id)
    survey["variable_columns"] = [column for column in survey["choices"][0] if (column != "name" and column != "seats")]

    # Check if the survey has answers. If it has, survey choices cannot be edited.
    survey_answers = survey_service.fetch_survey_responses(survey_id)
    edit_choices = True
    if len(survey_answers) > 0:
        edit_choices = False

    # Convert datetime.datetime(year, month, day, hour, minute) to date (dd.mm.yyyy) and time (hh:mm)
    start_date_data = survey["time_begin"]
    end_date_data = survey["time_end"]
    start_date = convert_date(start_date_data)
    end_date = convert_date(end_date_data)
    start_time = convert_time(start_date_data)
    end_time = convert_time(end_date_data)

    survey["start_time"] = start_time
    survey["end_time"] = end_time
    survey["start_date"] = start_date
    survey["end_date"] = end_date
 
    return render_template("edit_survey.html", survey=survey, survey_id = survey_id, edit_choices = edit_choices)

@app.route("/surveys/<string:survey_id>/edit", methods = ["POST"])
@teachers_only
def edit_survey_post(survey_id):
    """
    Post method for saving edits to a survey.
    """
    edit_dict = request.get_json()
    validation = survey_service.validate_created_survey(edit_dict, edited = True)
    if not validation["success"]:
        return jsonify(validation["message"]), 400

    user_id = session.get("user_id", 0)
    (success, message) = survey_service.save_survey_edit(survey_id, edit_dict, user_id)
    if not success:
        response = {"status":"0", "msg":message}
        return jsonify(response)
    response = {"status":"1", "msg":message}
    return jsonify(response)


@app.route("/surveys/<string:survey_id>/delete")
@teachers_only
def delete_survey(survey_id):
    #TODO
    ...

@app.route("/surveys/<string:survey_id>/edit/add_teacher/<string:teacher_email>", methods=["POST"])
@teachers_only
def add_teacher(survey_id, teacher_email):
    if not teacher_email:
        response = {"status":"0","msg":"Sähköpostiosoite puuttuu!"}
        return jsonify(response)
    (success, message) = survey_teachers_service.add_teacher_to_survey(survey_id, teacher_email)
    if not success:
        response = {"status":"0","msg":message}
        return jsonify(response)
    response = {"status":"1","msg":message}
    return jsonify(response)

@app.route("/surveys/<string:survey_id>/group_sizes", methods=["GET"])
@teachers_only
def edit_group_sizes(survey_id):
    """
    Edit group sizes in a survey and display total number of spaces vs answers
    Args:
        survey_id (int): id of the survey
    """
    survey = survey_service.get_survey_as_dict(survey_id)
    survey["variable_columns"] = [column for column in survey["choices"][0] if (column != "name" and column != "seats" and column != "id")]
    (survey_answers_amount, choice_popularities) = survey_service.get_choice_popularities(survey_id)
    available_spaces = survey_choices_service.count_number_of_available_spaces(survey_id)
    return render_template("group_sizes.html", survey_id=survey_id, survey=survey, survey_answers_amount=survey_answers_amount,
                            available_spaces=available_spaces, popularities = choice_popularities)

@app.route("/surveys/<string:survey_id>/group_sizes", methods=["POST"])
@teachers_only
def post_group_sizes(survey_id):
    """
    Post method for editing group sizes in the survey
    Args:
        survey_id (int): id of the survey
    """
    data = request.get_json()

    #validation would be here
    #if not validation["success"]:
    #    return jsonify(validation["message"]), 400

    #update_survey_group_sizes works when survey_choices is a list of dictionaries
    #just like what is used in create survey
    db_response = survey_service.update_survey_group_sizes(survey_id, data["choices"])
    response = {}
    if db_response[0] is True:
        response["status"] = "1"
        response["msg"] = "Tallennus onnistui. Päivitä sivu nähdäksesi tilanne"
    else:
        response["status"] = "0"
        response["msg"] = "Tallennus epäonnistui."

    return jsonify(response)

@app.route("/surveys/<string:survey_id>/answers", methods = ["GET"])
@ad_login
@teachers_only
def survey_answers(survey_id):
    """
    For displaying the answers of a survey
    """
    # If the results have been saved, redirect to the results page
    if survey_service.check_if_survey_results_saved(survey_id):
        return survey_results(survey_id)

    survey_name = survey_service.get_survey_name(survey_id)
    survey_answers = survey_service.fetch_survey_responses(survey_id)
    choices_data = []
    for s in survey_answers:
        choices_data.append([user_service.get_email(s[0]), s[1], s[2], s[3]])

    survey_answers_amount = len(survey_answers)
    available_spaces = survey_choices_service.count_number_of_available_spaces(survey_id)
    closed = survey_service.check_if_survey_closed(survey_id)
    answers_saved = survey_service.check_if_survey_results_saved(survey_id)
    error_message = "Ei voida luoda ryhmittelyä, koska vastauksia on enemmän kuin jaettavia paikkoja. Voit muuttaa jaettavien paikkojen määrän kyselyn muokkaus sivulta."
    return render_template("survey_answers.html",
                           survey_name=survey_name, survey_answers=choices_data,
                           survey_answers_amount=survey_answers_amount, available_spaces = available_spaces,
                           survey_id = survey_id, closed = closed, answered = answers_saved, error_message = error_message)

@app.route("/surveys/<string:survey_id>/results", methods = ["GET", "POST"])
@ad_login
@teachers_only
def survey_results(survey_id):
    """
    Display results of sorting students to groups.
    For the post request, the answers are saved to the database.
    """
    # Check that the survey is closed. If it is open, redirect to home page.
    if not survey_service.check_if_survey_closed(survey_id):
        return redirect('/')
    # Check if the answers are already saved to the database. This determines which operations are available to the teacher.
    saved_result_exists = survey_service.check_if_survey_results_saved(survey_id)

    # Check if there are more rankings than available slots
    available_spaces = survey_choices_service.count_number_of_available_spaces(survey_id)
    user_rankings = survey_service.fetch_survey_responses(survey_id)

    if not user_rankings:
        return redirect(f"/surveys/{survey_id}/answers")
    survey_answers_amount = len(user_rankings)

    #if more rankings than available slots add a non-group
    if (survey_answers_amount > available_spaces):
        added_group = survey_choices_service.add_empty_survey_choice(survey_id, survey_answers_amount-available_spaces)
        if not added_group:
            response = {"status":"0", "msg":"Ryhmäjako epäonnistui"}
            return jsonify(response)

    # Create the dictionaries with the correct data, so that the Hungarian algorithm can generate the results.
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    groups_dict = convert_choices_groups(survey_choices)
    students_dict = convert_users_students(user_rankings)
    weights = w.Weights(len(groups_dict), len(students_dict)).get_weights()
    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()

    # create an dict which contains choice's additional info as list
    additional_infos = {}
    for row in survey_choices:
        additional_infos[str(row[0])] = []
        
        cinfos = survey_choices_service.get_choice_additional_infos(row[0])
        for i in cinfos:
            additional_infos[str(row[0])].append(i[1])

    # Add to data the number of the choice the user got
    for results in output_data[0]:
        user_id = results[0][0]
        choice_id =  results[2][0]
        ranking = user_rankings_service.get_user_ranking(user_id, survey_id)
        happiness = get_happiness(choice_id, ranking)
        results.append(happiness)

    if request.method == "GET":
        return render_template("results.html", survey_id = survey_id, results = output_data[0],
                            happiness_data = output_data[2], happiness = output_data[1], answered = saved_result_exists,
                            infos=additional_infos, sc=cinfos)

    # If the request is post, check if results have been saved. If they have, redirect to previous_surveys page.
    if saved_result_exists:
        return redirect('/surveys')

    # Update the database entry for the survey, so that result_saved = True.
    survey_answered = survey_service.update_survey_answered(survey_id)
    if not survey_answered:
        return redirect('/surveys')

    # Create new database entrys for final groups of the sorted students.
    for results in output_data[0]:
        user_id = results[0][0]
        choice_id =  results[2][0]
        saved = final_group_service.save_result(user_id, survey_id, choice_id)
        if not saved:
            response = {"msg":f"ERROR IN SAVING {results[0][1]} RESULTS!"}
            return jsonify(response)
    return redirect('/surveys')

@app.route("/surveys/<string:survey_id>/close", methods = ["POST"])
@teachers_only
def close_survey(survey_id):
    """
    Close survey, so that no more answers can be submitted
    """
    user_id = session.get("user_id",0)
    closed = survey_service.close_survey(survey_id, user_id)
    if not closed:
        response = {"status":"0", "msg":"Kyselyn sulkeminen epäonnistui"}
        return jsonify(response)
    return redirect(f'/surveys/{survey_id}/answers')

@app.route("/surveys/<string:survey_id>/open", methods = ["POST"])
@teachers_only
def open_survey(survey_id):
    """
    Open survey back up so that students can submit answers
    """
    user_id = session.get("user_id",0)
    opened = survey_service.open_survey(survey_id, user_id)
    if not opened:
        response = {"status":"0", "msg":"Kyselyn avaaminen epäonnistui"}
        return jsonify(response)
    return redirect(f'/surveys/{survey_id}/answers')

"""
/AUTH/* ROUTES:
"""
@app.route("/auth/login", methods = ["GET", "POST"])
def login():
    if not app.debug:
        return redirect("/")
    
    users = [User("outi1", "testi.opettaja@helsinki.fi", True),
             User("olli1", "testi.opiskelija@helsinki.fi", False),
             User("robottiStudent", "robotti.student@helsinki.fi", False),
             User("robottiTeacher", "robotti.teacher@helsinki.fi", True),
             User("robottiTeacher2", "robotti.2.teacher@helsinki.fi", True)]
    
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

        if not user_service.find_by_email(email): # account doesn't exist, register
            user_service.create_user(name, email, role_bool) # actual registration
        if user_service.check_credentials(email): # log in, update session etc.
            if role_bool:
                user_service.make_user_teacher(email)

        return redirect("/")
        

@app.route("/auth/logout")
def logout():

    user_service.logout()

    # stupid, but Openshift getenv() can't find Openshift secrets,
    # so here we are
    if app.debug:
        return redirect("/")
    else:
        return redirect("/Shibboleth.sso/Logout")
    

"""
ADMINTOOLS -ROUTES:
"""
@app.route("/admintools/analytics")
def admin_analytics():
    # Only admins permitted!
    user_id = session.get("user_id",0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    data = []
    all_created_surveys = survey_service.len_all_surveys()
    all_active_surveys = survey_service.len_active_surveys()
    all_students = user_service.len_all_students()
    all_student_rankings = user_rankings_service.len_all_rankings()
    all_teachers =user_service.len_all_teachers()

    data.append(all_created_surveys)
    data.append(all_active_surveys)
    data.append(all_students)
    data.append(all_student_rankings)
    data.append(all_teachers)

    return render_template("admintools/admin_analytics.html", data = data)

@app.route("/admintools/feedback")
def admin_feedback():
    # Only admins permitted!
    user_id = session.get("user_id",0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    data = feedback_service.get_unsolved_feedback()

    return render_template("admintools/admin_feedback.html", data = data)

@app.route("/admintools/feedback/closed")
def admin_closed_feedback():
    # Only admins permitted!
    user_id = session.get("user_id",0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    data = feedback_service.get_solved_feedback()

    return render_template("admintools/admin_closed_feedback.html", data = data)

@app.route("/admintools/feedback/<int:feedback_id>")
def admin_feedback_data(feedback_id):
    # Only admins permitted!
    user_id = session.get("user_id",0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")

    feedback = feedback_service.get_feedback(feedback_id)
    if not feedback:
        return redirect("/")
    return render_template("admintools/admin_feedback_data.html", feedback = feedback)

@app.route("/admintools/feedback/<int:feedback_id>/close", methods = ["POST"])
def admin_feedback_close_feedback(feedback_id):
    # Only admins permitted!
    user_id = session.get("user_id",0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")
    success = feedback_service.mark_feedback_solved(feedback_id)
    if not success:
        return redirect("/")
    return redirect("/admintools/feedback")

@app.route("/admintools/surveys", methods = ["GET"])
def admin_all_active_surveys():
    # Only admins permitted!
    user_id = session.get("user_id",0)
    admin = user_service.check_if_admin(user_id)
    if not admin:
        return redirect("/")
    data = survey_service.get_all_active_surveys()
    if not data:
        return redirect("/")
    return render_template("/admintools/admin_survey_list.html", data = data)

"""
MISCELLANEOUS ROUTES:
"""
@app.route("/privacy-policy")
def privacy_policy():
    """
    Route returns the Privacy Policy -page linked in the footer
    """
    privacy_policy_file = Path(__file__).parents[0] / 'static' / 'content' / 'Tietosuojaseloste.md'
    content = open(privacy_policy_file, 'r', encoding='utf-8').read()
    return render_template("content-page.html", content=markdown.markdown(content), title="Tietosuojaseloste")

@app.route("/faq")
def faq():
    """
    Route returns the Frequently Asked Questions -page linked in the footer
    """
    faq_file = Path(__file__).parents[0] / 'static' / 'content' / 'faq.md'
    content = open(faq_file, 'r', encoding='utf-8').read()
    return render_template("content-page.html", content=markdown.markdown(content), title="UKK")

@app.route("/csv-instructions")
def csv_instructions():
    """
    Route returns the Privacy Policy -page linked in the footer
    """
    csv_file = Path(__file__).parents[0] / 'static' / 'content' / 'csv-instructions.md'
    content = open(csv_file, 'r', encoding='utf-8').read()
    return render_template("content-page.html", content=markdown.markdown(content), title="Tietosuojaseloste")

@app.route("/excel")
def excel():
    """
    Performance test for the Hungarian algortihm with real life data.
    """
    groups_dict = excelreader.create_groups()
    students_dict = excelreader.create_students(groups_dict)
    weights = w.Weights(len(groups_dict), len(students_dict)).get_weights()

    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()
    return render_template("results.html", results = output_data[0],
                           happiness_data = output_data[2], happiness = output_data[1])

@app.route("/get_choices/<string:survey_id>", methods=["POST"])
def get_choices(survey_id):
    """
    Save the ranking to the database.
    """
    raw_data = request.get_json()

    # list of ids of choices not put in either of the boxes
    neutral_ids = raw_data["neutralIDs"]

    # list of ids of choices put in red box
    bad_ids = raw_data["badIDs"]

    #list of ids of choices put in green box
    good_ids = raw_data["goodIDs"]

    #list of all ids
    all_ids = raw_data["allIDs"]

    #value of textarea reasons
    reason = raw_data["reasons"]

    #minimum number of choices in the green box
    min_choices = int(raw_data["minChoices"])

    #maximum number of choices in the red box
    allowed_denied_choices = int(raw_data["maxBadChoices"])

    if len(good_ids) < min_choices:
        response = {"status":"0","msg":f"Valitse vähintään {min_choices} vaihtoehtoa. Tallennus epäonnistui."}
        return jsonify(response)

    if len(bad_ids) > allowed_denied_choices:
        response = {"status":"0","msg":f"Voit hylätä korkeintaan {allowed_denied_choices} vaihtoehtoa. Tallennus epäonnistui."}
        return jsonify(response)

    ranking = convert_to_string(good_ids)
    rejections = convert_to_string(bad_ids)

    # Verify that if user has rejections, they have also added a reasoning for them.
    if len(bad_ids) == 0 and len(reason) > 0:
        response = {"status":"0","msg":"Ei hyväksytä perusteluita, jos ei ole hylkäyksiä! Tallennus epäonnistui."}
        return jsonify(response)

    # Verify that the reasoning isn't too long or short.
    if len(reason) > 300:
        response = {"status":"0","msg":"Perustelu on liian pitkä, tallenus epäonnistui. Merkkejä saa olla korkeintaan 300. Tarvittaessa ota yhteys kyselyn järjestäjään."}
        return jsonify(response)
    if len(reason) < 10 and len(bad_ids) > 0:
        response = {"status":"0","msg":"Perustelu on liian lyhyt, tallennus epäonnistui. Merkkeja tulee olla vähintään 10."}
        return jsonify(response)

    user_id = session.get("user_id",0)
    submission = user_rankings_service.add_user_ranking(user_id, survey_id, ranking, rejections, reason)
    response = {"status":"1","msg":"Tallennus onnistui."}
    if not submission:
        response = {"status":"0","msg":"Tallennus epäonnistui."}
    return jsonify(response)

@app.route("/feedback", methods = ["GET", "POST"])
def feedback():
    if request.method == "GET":
        return render_template("feedback.html")
    user_id = session.get("user_id",0)
    data = request.get_json()
    (success, message) = feedback_service.new_feedback(user_id, data)
    response = {"status":"1","msg":message}
    if not success:
        response = {"status":"0","msg":message}
    return jsonify(response)

"""
TASKS:
"""
@scheduler.task('cron', id='close_surveys', hour='*')
def close_surveys():
    """
    Every hour go through a list of a all open surveys. Close all surveys which have an end_date equal or less to now
    """
    with app.app_context():
        survey_service.check_for_surveys_to_close()
