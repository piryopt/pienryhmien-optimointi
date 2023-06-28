import os
from flask import render_template, request, session, jsonify, redirect
from sqlalchemy import text
import psycopg2
from pathlib import Path
from random import shuffle
from src import app,db
from src.services.user_service import user_service
from src.services.survey_service import survey_service
from src.tools import data_gen, excelreader
import src.algorithms.hungarian as h
import src.algorithms.weights as w
from src.services.survey_tools import SurveyTools

# Globals
CONNECTION_URL = os.getenv("DATABASE_URL")

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    print(f'HEADERS:\n{request.headers["Connection"]}')
    return render_template('index.html')



@app.route("/db_connection_test")
def db_connection_test():
    conn = None
    try:
        conn = psycopg2.connect(CONNECTION_URL)
        cursor = conn.cursor()
        sql = "SELECT * FROM users"
        cursor.execute(text(sql))
        for i in cursor.fetchall():
            print(i)
        conn.close()
        sql = "SELECT * FROM users"
        result = db.session.execute(text(sql))
        user = result.fetchone()
        print(user)
        #return "<pre><code>" + str(conn) + "</code></pre>"
        return user.email
    except Exception as e:
        conn.close()
        print(e)
        return "<code>" + str(e) + "</code>"

@app.route("/input")
def input() -> str:
    return render_template('input.html')

@app.route("/results", methods = ["POST"])
def results():
    group_n = int(request.form.get("group_n"))
    student_n = int(request.form.get("student_n"))
    group_size = int(request.form.get("group_size"))

    groups_dict = data_gen.generate_groups(group_n, group_size)
    students_dict = data_gen.generate_students(student_n, groups_dict)
    weights = w.Weights(group_n, student_n, True).get_weights()

    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()
    return render_template("results.html", results = output_data[0], happiness_data = output_data[3],
                           time = output_data[1], happiness = output_data[2])

@app.route("/excel")
def excel():
    groups_dict = excelreader.create_groups()
    students_dict = excelreader.create_students(groups_dict)
    weights = w.Weights(len(groups_dict), len(students_dict), True).get_weights()

    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()
    return render_template("results.html", results = output_data[0], happiness_data = output_data[3],
                           time = output_data[1], happiness = output_data[2])

@app.route("/surveys/<int:survey_id>")
def surveys(survey_id):
    survey_choices = survey_service.get_list_of_survey_choices(survey_id)
    shuffle(survey_choices)
    if not survey_choices or session.get("user_id", 0) == 0:
        print("SURVEY DOES NOT EXIST OR NOT LOGGED IN!")
        return render_template("index.html")
    survey_name = survey_service.get_survey_name(survey_id)
    existing = "0"
    user_id = session.get("user_id", 0)
    user_survey_ranking = survey_service.user_ranking_exists(survey_id, user_id)

    if user_survey_ranking:
        existing = "1"
        user_rankings = user_survey_ranking[3]
        list_of_survey_choice_id = user_rankings.split(",")

        survey_choices = []
        for survey_choice_id in list_of_survey_choice_id:
            survey_choice = survey_service.get_survey_choice(survey_choice_id)
            if not survey_choice:
                continue
            survey_choices.append(survey_choice)
    return render_template("survey.html", choices = survey_choices, survey_id = survey_id, survey_name = survey_name, existing = existing)

@app.route("/surveys/<int:survey_id>/deletesubmission", methods=["POST"])
def delete_submission(survey_id):
    response = {"status":"0", "msg":"Poistaminen epäonnistui"}
    current_user_id = session.get("user_id", 0)
    if survey_service.delete_ranking(survey_id, current_user_id):
        response = {"status":"1", "msg":"Valinnat poistettu"}
    return jsonify(response)

@app.route("/get_choices/<int:survey_id>", methods=["POST"])
def get_choices(survey_id):
    raw_data = request.get_json()
    ranking = ','.join(raw_data)
    user_id = session.get("user_id",0)
    submission = survey_service.add_user_ranking(survey_id, ranking, user_id)
    response = {"status":"1","msg":"Tallennus onnistui."}
    if not submission:
        response = {"status":"0","msg":"Tallennus epäonnistui."}
    return jsonify(response)

@app.route("/surveys/getinfo", methods=["POST"])
def get_info():
    raw_id = request.get_json()
    choice_info = survey_service.get_survey_choice(int(raw_id))
    return render_template("moreinfo.html", choice_info = choice_info)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    email = request.form.get("email")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    student_number = request.form.get("student_number")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")
    isteacher = request.form.get("isteacher")
    teacher_priv = False
    if isteacher == "teacher":
        teacher_priv = True

    new_user = user_service.create_user(firstname, lastname, student_number, email, password1, password2, teacher_priv)
    if new_user is None:
        return render_template("register.html")
    return render_template("login.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email")
    password = request.form.get("password")

    logged_in = user_service.check_credentials(email, password)
    if not logged_in:
        return render_template("login.html")
    return render_template("index.html")

@app.route("/logout")
def logout():
    user_service.logout()
    return render_template("index.html")

@app.route("/groups")
def groups():
    return render_template("groups.html")

@app.route("/create_survey", methods = ["GET"])
def new_survey_form():
    return render_template("create_survey.html")

@app.route("/create_survey", methods = ["POST"])
def new_survey_post():
    data = request.get_json()
    survey_name = data["surveyGroupname"]
    new_survey_id = survey_service.add_new_survey(survey_name)
    if not new_survey_id:
        return redirect("create_survey.html")
    survey_choices = data["choices"]
    for choice in survey_choices:
        choice_name = choice["choiceName"]
        max_spaces = choice["choiceMaxSpaces"]
        info1 = choice["choiceInfo1"]
        info2 = choice["choiceInfo2"]
        survey_service.add_survey_choice(new_survey_id, choice_name, max_spaces, info1, info2)

    response = {"msg":"Uusi kysely luotu!"}
    return jsonify(response)

@app.route("/previous_surveys")
def previous_surveys():
    '''For fetching previous survey list from the database'''
    #search_results = SurveyTools.fetch_surveys_and_answer_amounts() 
    search_results = SurveyTools.fetch_all_surveys()
    return render_template("surveys.html", search_results=search_results)

@app.route("/survey_answers", methods = ["post"])
def survey_answers():
    '''For displaying answers on a certain survey'''
    survey_id = request.form["survey_id"]
    survey_name = request.form["survey_name"]
    survey_answers = SurveyTools.fetch_survey_responses(survey_id)
    survey_answers_amount = len(survey_answers)
    return render_template("survey_answers.html",
                           survey_name=survey_name, survey_answers=survey_answers,
                           survey_answers_amount=survey_answers_amount)

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
