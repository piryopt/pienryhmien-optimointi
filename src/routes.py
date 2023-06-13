import os
from flask import render_template, request, redirect, jsonify
from app import app
import algorithms.hungarian as h
import algorithms.weights as w
from tools import data_gen, excelreader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

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
        conn.close()
        return "<pre><code>" + str(conn) + "</code></pre>"
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
    conn = None
    try:
        conn = psycopg2.connect(connection_uri)

        sql = "SELECT id, name, info1, info2 FROM choices WHERE survey_id=:survey_id"
        group_choices = [(0,"Ryhmä1","ohjaaja1","osoite1"),(1,"Ryhmä2","ohjaaja2","osoite2"),(2,"Ryhmä3","ohjaaja3","osoite3")]

        conn.close()
    except Exception as e:
        conn.close()
        print(e)
        return "Database connection error: " + e

    return render_template("survey.html", choices = group_choices)

@app.route("/get_choices", methods=["POST"])
def get_choices():
    raw_data = request.get_json()
    choices = [int(i) for i in raw_data]
    response = {"msg":"Tallennus onnistui."}
    return jsonify(response)
