from pathlib import Path
from sqlalchemy import text
from random import shuffle
from functools import wraps
from flask import render_template, request, session, jsonify, redirect, url_for
from src import app,db
from src.services.user_service import user_service
from src.services.survey_service import survey_service
from src.services.survey_choices_service import survey_choices_service
from src.services.user_rankings_service import user_rankings_service
from src.services.final_group_service import final_group_service
from src.tools import data_gen, excelreader
import src.algorithms.hungarian as h
import src.algorithms.weights as w
from src.services.survey_tools import SurveyTools
from src.tools.db_data_gen import gen_data
from src.tools.survey_result_helper import convert_choices_groups, convert_users_students, get_happiness
from src.tools.rankings_converter import convert_to_list, convert_to_string
from src.tools.parsers import parser_elomake_csv_to_dict
from functools import wraps

def home_decorator():
    def _home_decorator(f):
        @wraps(f)
        def __home_decorator(*args, **kwargs):
            # just do here everything what you need
            result = f(*args, **kwargs)

            name = request.headers.get('cn')
            email = request.headers.get('mail')
            student_number = request.headers.get('hyPersonStudentId')

            # Array of strings of user's roles
            roles = request.headers.get('eduPersonAffiliation')

            role_bool = True if "faculty" in roles or "staff" in roles else False

            print("Nimi", name)
            print("Rooli", roles)
            print("Sposti", email)
            print("Numero", student_number)


            uid = session.get("user_id", 0) # check if logged in already 
            if uid == 0:
                if not user_service.find_by_email(email): # account doesn't exist, register
                    user_service.create_user(name, student_number, email, role_bool) # actual registration
                if user_service.check_credentials(email): # log in, update session etc.
                    if role_bool:
                        user_service.make_user_teacher(email)

            return result
        return __home_decorator
    return _home_decorator

@app.route("/")
@home_decorator()
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    #print(f'HEADERS:\n{request.headers["Connection"]}')
    user_id = session.get("user_id",0)
    surveys_created = survey_service.count_surveys_created(user_id)
    if surveys_created == 0:
        return render_template('index.html', surveys_created = 0, exists = False)
    surveys = survey_service.get_active_surveys(user_id)
    if not surveys:
        return render_template('index.html', surveys_created = surveys_created, exists = False)
    data = []
    for s in surveys:
        survey_id = s[0]
        surveyname = s[1]
        survey_answers = SurveyTools.fetch_survey_responses(survey_id)
        participants = len(survey_answers)
        # VAIHDA TÄMÄ OIKEESEEN PÄIVÄMÄÄRÄÄN KUN SAADAAN TOIMINNALLISUUS!!
        survey_ending_date = survey_service.get_survey_enddate(survey_id)
        data.append([survey_id, surveyname, participants, survey_ending_date])

    return render_template('index.html', surveys_created = surveys_created, exists = True, data = data, error_statement = "DOES THIS WORK?")


@app.route("/results", methods = ["POST"])
def results():
    group_n = int(request.form.get("group_n"))
    student_n = int(request.form.get("student_n"))
    group_size = int(request.form.get("group_size"))

    groups_dict = data_gen.generate_groups(group_n, group_size)
    students_dict = data_gen.generate_students(student_n, groups_dict)
    weights = w.Weights(group_n, student_n).get_weights()

    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()
    return render_template("results.html", results = output_data[0],
                           happiness_data = output_data[2], happiness = output_data[1])

@app.route("/excel")
def excel():
    '''Performance test for the Hungarian algortihm with real life data.'''
    groups_dict = excelreader.create_groups()
    students_dict = excelreader.create_students(groups_dict)
    weights = w.Weights(len(groups_dict), len(students_dict)).get_weights()

    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()
    return render_template("results.html", results = output_data[0],
                           happiness_data = output_data[2], happiness = output_data[1])

@app.route("/surveys/<int:survey_id>")
def surveys(survey_id):
    '''The answer page for surveys.'''
    # If the survey has no choices, redirect to home page.
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    desc = survey_service.get_survey_description(survey_id)
    if not survey_choices or session.get("user_id", 0) == 0:
        print("SURVEY DOES NOT EXIST OR NOT LOGGED IN!")
        return hello_world()

    # Shuffle the choices, so that the choices aren't displayed in a fixed order.
    shuffle(survey_choices)

    closed = survey_service.check_if_survey_closed(survey_id)
    survey_name = survey_service.get_survey_name(survey_id)
    existing = "0"
    user_id = session.get("user_id", 0)
    user_survey_ranking = user_rankings_service.user_ranking_exists(survey_id, user_id)
    enddate = survey_service.get_survey_enddate(survey_id)

    # If a ranking exists, display the choices in the order that the student chose them.
    if user_survey_ranking:
        existing = "1"
        user_rankings = user_survey_ranking[3]
        list_of_survey_choice_id = convert_to_list(user_rankings)

        survey_choices = []
        for survey_choice_id in list_of_survey_choice_id:
            survey_choice = survey_choices_service.get_survey_choice(survey_choice_id)
            if not survey_choice:
                continue
            survey_choices.append(survey_choice)

    # If the survey is closed, return a different page, where the student can view their answers.
    if closed:
        if user_survey_ranking:
            return render_template("closedsurvey.html", choices = survey_choices, survey_name = survey_name)
        return render_template("closedsurvey.html", survey_name = survey_name)

    return render_template("survey.html", choices = survey_choices, survey_id = survey_id,
                            survey_name = survey_name, existing = existing, spaces = "Ryhmän maksimikoko: 10", desc = desc, enddate = enddate)

@app.route("/surveys/<int:survey_id>/deletesubmission", methods=["POST"])
def delete_submission(survey_id):
    '''Delete the current ranking of the student.'''
    response = {"status":"0", "msg":"Poistaminen epäonnistui"}
    current_user_id = session.get("user_id", 0)
    if user_rankings_service.delete_ranking(survey_id, current_user_id):
        response = {"status":"1", "msg":"Valinnat poistettu"}
    return jsonify(response)

@app.route("/get_choices/<int:survey_id>", methods=["POST"])
def get_choices(survey_id):
    '''Save the ranking to the database.'''
    raw_data = request.get_json()
    ranking = convert_to_string(raw_data)
    user_id = session.get("user_id",0)
    submission = user_rankings_service.add_user_ranking(survey_id, ranking, user_id)
    response = {"status":"1","msg":"Tallennus onnistui."}
    if not submission:
        response = {"status":"0","msg":"Tallennus epäonnistui."}
    return jsonify(response)

@app.route("/surveys/getinfo", methods=["POST"])
def get_info():
    raw_id = request.get_json()
    basic_info = survey_choices_service.get_choice_name_and_spaces(int(raw_id))
    additional_info = survey_choices_service.get_choice_additional_infos(int(raw_id))
    return render_template("moreinfo.html", basic = basic_info, infos = additional_info)

@app.route("/register", methods = ["GET", "POST"])
def register():
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
        return render_template("register.html")
    return render_template("login.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")

    logged_in = user_service.check_credentials(email)
    if not logged_in:
        return render_template("login.html")
    return hello_world()

@app.route("/logout")
def logout():
    user_service.logout()
    return render_template("index.html")

@app.route("/create_survey", methods = ["GET"])
def new_survey_form(survey=None):
    return render_template("create_survey.html", survey=survey)

@app.route("/create_survey", methods = ["POST"])
def new_survey_post():
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

    print("Alkaa", date_begin, time_begin)
    print("Alkaa", date_end, time_end)

    try:
        survey_service.create_new_survey_manual(survey_choices, survey_name, user_id, description, minchoices, date_begin, time_begin, date_end, time_end)
        response = {"msg":"Uusi kysely luotu!"}
        return jsonify(response)
    except: 
        return (jsonify({"msg": "Tuntematon virhe palvelimella"}), 500)
    

@app.route("/create_survey/import", methods = ["POST"])
def import_survey_choices():
    data = request.get_json()
    return jsonify(parser_elomake_csv_to_dict(data['uploadedFileContent'])["choices"])

@app.route("/previous_surveys")
def previous_surveys():
    '''For fetching previous survey list from the database'''
    user_id = session.get("user_id",0)
    if user_id == 0:
        return hello_world()
    active_surveys = SurveyTools.fetch_all_active_surveys(user_id)
    closed_surveys = survey_service.get_list_closed_surveys(user_id)
    return render_template("surveys.html", active_surveys=active_surveys, closed_surveys = closed_surveys)

@app.route("/surveys/<int:survey_id>/answers", methods = ["GET"])
def survey_answers(survey_id):
    '''For displaying the answers of a certain survey'''
    # If the results have been saved, redirect to the ersults page
    if survey_service.check_if_survey_results_saved(survey_id):
        return survey_results(survey_id)
    survey_name = survey_service.get_survey_name(survey_id)
    survey_answers = SurveyTools.fetch_survey_responses(survey_id)
    choices_data = []
    for s in survey_answers:
        choices_data.append([user_service.get_email(s[0]), s[1]])
    survey_answers_amount = len(survey_answers)
    closed = survey_service.check_if_survey_closed(survey_id)
    answers_saved = survey_service.check_if_survey_results_saved(survey_id)
    return render_template("survey_answers.html",
                           survey_name=survey_name, survey_answers=choices_data,
                           survey_answers_amount=survey_answers_amount, survey_id = survey_id, closed = closed,
                           answered = answers_saved)

@app.route("/admintools/", methods = ["GET"])
def admin_dashboard() -> str:
    return render_template('/admintools/dashboard.html')

@app.route("/api/admintools/reset", methods = ["POST"])
def reset_database() -> str:
    '''Drop all database tables and recreate them based on the schema at project root'''
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
    '''Page for generating users, a survey and user rankings.'''
    user_id = session.get("user_id",0)
    surveys = SurveyTools.fetch_all_active_surveys(user_id)
    if request.method == "GET":
        return render_template("/admintools/gen_data.html", surveys = surveys)

    if request.method == "POST":
        student_n = request.form.get("student_n")
        gen_data.generate_users(int(student_n))
        gen_data.add_generated_users_db()
        return render_template("/admintools/gen_data.html", surveys = surveys)

@app.route("/admintools/gen_data/rankings", methods = ["POST"])
def admin_gen_rankings():
    '''Generate user rankings for a survey (chosen from a list) for testing.'''
    survey_id = request.form.get("survey_list")
    survey_name = survey_service.get_survey_name(survey_id)
    gen_data.generate_rankings(survey_id)

    survey_answers = SurveyTools.fetch_survey_responses(survey_id)
    survey_answers_amount = len(survey_answers)
    return render_template("survey_answers.html",
                           survey_name=survey_name, survey_answers=survey_answers,
                           survey_answers_amount=survey_answers_amount, survey_id = survey_id)

@app.route("/admintools/gen_data/survey", methods = ["POST"])
def admin_gen_survey():
    '''Generate a survey for testing.'''
    user_id = session.get("user_id",0)
    gen_data.generate_survey(user_id)
    surveys = SurveyTools.fetch_all_active_surveys(user_id)
    return render_template("/admintools/gen_data.html", surveys = surveys)

@app.route("/surveys/<int:survey_id>/results", methods = ["GET", "POST"])
def survey_results(survey_id):
    '''Display survey results. For the post request, the answers are saved to the database.'''

    # Check that the survey is closed. If it is open, redirect to home page.
    if not survey_service.check_if_survey_closed(survey_id):
        return hello_world()
    # Check if the answers are already saved to the database. This determines which operations are available to the teacher.
    saved_result_exists = survey_service.check_if_survey_results_saved(survey_id)

    # Create the dictionaries with the correct data, so that the Hungarian algorithm can generate the results.
    survey_choices = survey_choices_service.get_list_of_survey_choices(survey_id)
    user_rankings = SurveyTools.fetch_survey_responses(survey_id)
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
        print("Results have already been saved!")
        return previous_surveys()

    # Update the database entry for the survey, so that result_saved = True.
    survey_answered = survey_service.update_survey_answered(survey_id)
    if not survey_answered:
        return previous_surveys()

    # Create new database entrys for final groups of the sorted students.
    for results in output_data[0]:
        user_id = results[0][0]
        choice_id =  results[2][0]
        saved = final_group_service.save_result(user_id, survey_id, choice_id)
        if not saved:
            print(f"ERROR IN SAVING {results[0][1]} RESULTS!")
    return previous_surveys()

@app.route("/surveys/<int:survey_id>/close", methods = ["POST"])
def close_survey(survey_id):
    '''Close survey, so that no more answers can be submitted'''
    user_id = session.get("user_id",0)
    closed = survey_service.close_survey(survey_id, user_id)
    if not closed:
        print("ERROR IN CLOSING SURVEY")
    return survey_answers(survey_id)

@app.route("/surveys/<int:survey_id>/open", methods = ["POST"])
def open_survey(survey_id):
    '''Open survey back up so that students can submit answers'''
    user_id = session.get("user_id",0)
    opened = survey_service.open_survey(survey_id, user_id)
    if not opened:
        print("ERROR IN OPENING SURVEY")
    return survey_answers(survey_id)
