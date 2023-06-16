import os
from flask import render_template, request, redirect, jsonify, session
from app import app
import algorithms.hungarian as h
import algorithms.weights as w
from tools import data_gen, excelreader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from services.user_service import user_service
from services.survey_service import survey_service

"""
GLOBALS
"""
connection_uri = os.getenv("DATABASE_URL")

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    return render_template('index.html')

@app.route("/db_connection_test")
def db_connection_test():
    conn = None
    try:
        conn = psycopg2.connect(connection_uri)
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

    return render_template("results.html", results = output_data.selections, happiness_data = output_data.happiness_data,
                           time = output_data.time, happiness = output_data.happiness)

@app.route("/excel")
def excel():
    groups_dict = excelreader.create_groups()
    students_dict = excelreader.create_students(groups_dict)
    weights = w.Weights(len(groups_dict), len(students_dict), True).get_weights()

    sort = h.Hungarian(groups_dict, students_dict, weights)
    sort.run()
    output_data = sort.get_data()

    return render_template("results.html", results = output_data.selections, happiness_data = output_data.happiness_data,
                           time = output_data.time, happiness = output_data.happiness)

@app.route("/surveys/<int:survey_id>")
def surveys(survey_id):
    survey_choices = survey_service.get_list_of_survey_choices(survey_id)
    if not survey_choices:
        print("SURVEY DOES NOT EXIST!")
        return render_template("index.html")
    return render_template("survey.html", choices = survey_choices, survey_id = survey_id)

@app.route("/get_choices/<int:survey_id>", methods=["POST"])
def get_choices(survey_id):
    raw_data = request.get_json()
    ranking = ','.join(raw_data)
    submission = survey_service.new_user_ranking(survey_id, ranking)
    response = {"msg":"Tallennus onnistui."}
    if not submission:
        response = {"msg":"Tallennus epäonnistui."}
    return jsonify(response)

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
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
        if new_user == None:
            return render_template("register.html")
        return render_template("login.html")
    
@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
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
