from pathlib import Path
from random import shuffle
from functools import wraps
from sqlalchemy import text
from flask import render_template, request, session, jsonify, redirect, url_for
from src import app,db
from src.repositories.survey_repository import survey_repository
from src.services.user_service import user_service
from src.services.survey_service import survey_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.services.final_group_service import final_group_service
from src.tools import excelreader
import src.algorithms.hungarian as h
import src.algorithms.weights as w
from src.tools.db_data_gen import gen_data
from src.tools.survey_result_helper import convert_choices_groups, convert_users_students, get_happiness
from src.tools.rankings_converter import convert_to_list, convert_to_string
from src.tools.parsers import parser_elomake_csv_to_dict

"""
DECORATORS:
"""
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
def frontpage() -> str:
    """
    Returns the rendered skeleton template
    """
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
        survey_answers = survey_repository.fetch_survey_responses(survey_id)
        participants = len(survey_answers)
        survey_ending_date = survey_service.get_survey_enddate(survey_id)
        data.append([survey_id, surveyname, participants, survey_ending_date])

    return render_template('index.html', surveys_created = surveys_created, exists = True, data = data, is_teacher = is_teacher)

"""
/SURVEYS/* ROUTES:
"""
@app.route("/surveys")
def previous_surveys():
    """
    For fetching previous survey list from the database
    """
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
    additional_info = survey_choices_service.get_choice_additional_infos(int(raw_id))
    return render_template("moreinfo.html", basic = basic_info, infos = additional_info)

@app.route("/surveys/create", methods = ["GET"])
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
        survey["variable_columns"] = [column for column in survey["choices"][0] if (column != "name" and column != "seats")]
    return render_template("create_survey.html", survey=survey)

@app.route("/surveys/create", methods = ["POST"])
@teachers_only
def new_survey_post():
    """
    Post method for creating a new survey.
    """
    data = request.get_json()
    survey_name = data["surveyGroupname"]
    description = data["surveyInformation"]
    user_id = session.get("user_id",0)
    survey_choices = data["choices"]
    minchoices = data["minchoices"]

    date_begin = data["startdate"]
    time_begin = data["starttime"]

    date_end = data["enddate"]
    time_end = data["endtime"]

    #print("Alkaa", date_begin, time_begin)
    #print("Alkaa", date_end, time_end)

    try:
        survey_service.create_new_survey_manual(survey_choices, survey_name, user_id, description, minchoices, date_begin, time_begin, date_end, time_end)
        response = {"msg":"Uusi kysely luotu!"}
        return jsonify(response)
    except:
        return (jsonify({"msg": "Tuntematon virhe palvelimella"}), 500)

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
@app.route("/surveys/<int:survey_id>")
def surveys(survey_id):
    """
    The answer page for surveys.
    """
    user_id = session.get("user_id",0)
    # If the survey has no choices, redirect to home page.
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    if not survey_choices or user_id == 0:
        return redirect("/")

    # Shuffle the choices, so that the choices aren't displayed in a fixed order.
    shuffle(survey_choices)

    desc = survey_service.get_survey_description(survey_id)
    closed = survey_service.check_if_survey_closed(survey_id)
    survey_name = survey_service.get_survey_name(survey_id)
    existing = "0"
    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    enddate = survey_service.get_survey_enddate(survey_id)

    # If a ranking exists, display the choices and the reasoning in the order that the student chose them.
    if user_survey_ranking:
        existing = "1"
        user_rankings = user_survey_ranking[3]
        rejections = user_survey_ranking[4]
        reason = user_survey_ranking[5]

        list_of_good_survey_choice_id = convert_to_list(user_rankings)

        good_survey_choices = []
        for survey_choice_id in list_of_good_survey_choice_id:
            survey_choice = survey_choices_service.get_survey_choice(survey_choice_id)
            if not survey_choice:
                continue
            good_survey_choices.append(survey_choice)
            survey_choices.remove(survey_choice)

        bad_survey_choices = []
        if len(rejections) > 0:
            list_of_bad_survey_choice_id = convert_to_list(rejections)
            for survey_choice_id in list_of_bad_survey_choice_id:
                survey_choice = survey_choices_service.get_survey_choice(survey_choice_id)
                if not survey_choice:
                    continue
                bad_survey_choices.append(survey_choice)
                survey_choices.remove(survey_choice)
        if closed:
            return render_template("closedsurvey.html", bad_survey_choices = bad_survey_choices, good_survey_choices=good_survey_choices, survey_name = survey_name)
        return render_template("survey.html", choices = survey_choices, survey_id = survey_id,
                            survey_name = survey_name, existing = existing, desc = desc,
                            bad_survey_choices = bad_survey_choices, good_survey_choices=good_survey_choices, reason=reason)



    # If the survey is closed, return a different page, where the student can view their answers.
    if closed:
        return render_template("closedsurvey.html", survey_name = survey_name)

    return render_template("survey.html", choices = survey_choices, survey_id = survey_id,
                            survey_name = survey_name, existing = existing, desc = desc, enddate = enddate)

@app.route("/surveys/<int:survey_id>/deletesubmission", methods=["POST"])
def delete_submission(survey_id):
    """
    Delete the current ranking of the student.
    """
    response = {"status":"0", "msg":"Poistaminen epäonnistui"}
    current_user_id = session.get("user_id", 0)
    if user_rankings_service.delete_ranking(survey_id, current_user_id):
        response = {"status":"1", "msg":"Valinnat poistettu"}
    return jsonify(response)

@app.route("/surveys/<int:survey_id>/edit")
@teachers_only
def edit_survey(survey_id):
    #TODO
    ...

@app.route("/surveys/<int:survey_id>/edit")
@teachers_only
def delete_survey(survey_id):
    #TODO
    ...

@app.route("/surveys/<int:survey_id>/answers", methods = ["GET"])
@teachers_only
def survey_answers(survey_id):
    """
    For displaying the answers of a survey
    """
    # If the results have been saved, redirect to the results page
    if survey_service.check_if_survey_results_saved(survey_id):
        return survey_results(survey_id)

    survey_name = survey_service.get_survey_name(survey_id)
    survey_answers = survey_repository.fetch_survey_responses(survey_id)
    choices_data = []
    for s in survey_answers:
        choices_data.append([user_service.get_email(s[0]), s[1], s[2], s[3]])

    survey_answers_amount = len(survey_answers)
    closed = survey_service.check_if_survey_closed(survey_id)
    answers_saved = survey_service.check_if_survey_results_saved(survey_id)
    return render_template("survey_answers.html",
                           survey_name=survey_name, survey_answers=choices_data,
                           survey_answers_amount=survey_answers_amount, survey_id = survey_id, closed = closed,
                           answered = answers_saved)

@app.route("/surveys/<int:survey_id>/results", methods = ["GET", "POST"])
@teachers_only
def survey_results(survey_id):
    """
    Display survey results. For the post request, the answers are saved to the database.
    """
    # Check that the survey is closed. If it is open, redirect to home page.
    if not survey_service.check_if_survey_closed(survey_id):
        return redirect('/')
    # Check if the answers are already saved to the database. This determines which operations are available to the teacher.
    saved_result_exists = survey_service.check_if_survey_results_saved(survey_id)

    # Create the dictionaries with the correct data, so that the Hungarian algorithm can generate the results.
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    user_rankings = survey_repository.fetch_survey_responses(survey_id)
    groups_dict = convert_choices_groups(survey_choices)
    students_dict = convert_users_students(user_rankings)
    weights = w.Weights(len(groups_dict), len(students_dict)).get_weights()
    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()

    # Add to data the number of the choice the user got
    for results in output_data[0]:
        user_id = results[0][0]
        choice_id =  results[2][0]
        ranking = user_rankings_service.get_user_ranking(user_id, survey_id)
        happiness = get_happiness(choice_id, ranking)
        results.append(happiness)

    if request.method == "GET":
        return render_template("results.html", survey_id = survey_id, results = output_data[0],
                            happiness_data = output_data[2], happiness = output_data[1], answered = saved_result_exists)

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

@app.route("/surveys/<int:survey_id>/close", methods = ["POST"])
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

@app.route("/surveys/<int:survey_id>/open", methods = ["POST"])
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
@app.route("/auth/register", methods = ["GET", "POST"])
def register():
    """
    Mock user registeration. DELETE BEFORE PRODUCTION!!!
    """
    if request.method == "GET":
        return render_template("register.html")
    email = request.form.get("email")
    name = request.form.get("name")
    student_number = request.form.get("student_number")
    isteacher = request.form.get("isteacher")
    teacher_priv = False
    if isteacher == "teacher":
        teacher_priv = True

    new_user = user_service.create_user(name, student_number, email, teacher_priv)
    if new_user is None:
        return redirect("/auth/register")
    return redirect("/auth/login")

@app.route("/auth/login", methods = ["GET", "POST"])
def login():
    """
    Mock user login. DELETE BEFORE PRODUCTION!!!
    """
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")

    logged_in = user_service.check_credentials(email)
    if not logged_in:
        return redirect("/auth/login")
    return redirect("/")

@app.route("/auth/logout")
def logout():
    """
    Mock user logout. DELETE BEFORE PRODUCTION?
    """
    user_service.logout()
    return redirect("/")

"""
ADMINTOOLS -ROUTES:
"""
@app.route("/admintools/", methods = ["GET"])
def admin_dashboard() -> str:
    """
    Admin page for resestting the database. DELETE BEFORE PRODUCTION!!!
    """
    return render_template('/admintools/dashboard.html')

@app.route("/api/admintools/reset", methods = ["POST"])
def reset_database() -> str:
    """
    Drop all database tables and recreate them based on the schema at project root. DELETE BEFORE PRODUCTION!!!
    """
    data = request.get_json()
    print(data)
    db.reflect()
    db.drop_all()
    create_clause = data["schema"]
    for statement in create_clause.split(";")[:-1]:
        db.session.execute(text(statement + ";"))
        db.session.commit()
    return "database reset"

@app.route("/admintools/gen_data", methods = ["GET", "POST"])
def admin_gen_data():
    """
    Page for generating users, a survey and user rankings. DELETE BEFORE PRODUCTION!!!
    """
    user_id = session.get("user_id",0)
    surveys = survey_repository.fetch_all_active_surveys(user_id)
    if request.method == "GET":
        return render_template("/admintools/gen_data.html", surveys = surveys)

    if request.method == "POST":
        student_n = request.form.get("student_n")
        gen_data.generate_users(int(student_n))
        gen_data.add_generated_users_db()
        return render_template("/admintools/gen_data.html", surveys = surveys)

@app.route("/admintools/gen_data/rankings", methods = ["POST"])
def admin_gen_rankings():
    """
    Generate user rankings for a survey (chosen from a list) for testing. DELETE BEFORE PRODUCTION!!!
    """
    survey_id = request.form.get("survey_list")
    survey_name = survey_service.get_survey_name(survey_id)
    gen_data.generate_rankings(survey_id)

    survey_answers = survey_repository.fetch_survey_responses(survey_id)
    survey_answers_amount = len(survey_answers)
    return render_template("survey_answers.html",
                           survey_name=survey_name, survey_answers=survey_answers,
                           survey_answers_amount=survey_answers_amount, survey_id = survey_id)

@app.route("/admintools/gen_data/survey", methods = ["POST"])
def admin_gen_survey():
    """
    Generate a survey for testing. DELETE BEFORE PRODUCTION!!!
    """
    user_id = session.get("user_id",0)
    gen_data.generate_survey(user_id)
    surveys = survey_repository.fetch_all_active_surveys(user_id)
    return render_template("/admintools/gen_data.html", surveys = surveys)

"""
MISCELLANEOUS ROUTES:
"""
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

@app.route("/get_choices/<int:survey_id>", methods=["POST"])
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

    # Change this to len bad_ids + good_ids >= min_choices
    # Also check that there aren't to many rejections.
    if len(neutral_ids) > 0 or len(good_ids) == 0:
        response = {"status":"0","msg":"Et ole tehnyt riittävän monta valintaa! Tallennus epäonnistui."}
        return jsonify(response)

    if len(bad_ids) > 2:
        response = {"status":"0","msg":"Liian monta hylkäystä! Tallennus epäonnistui."}
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
