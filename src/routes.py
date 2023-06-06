import os

from flask import render_template, request
from app import app
from copy import deepcopy
import algorithms.hungarian as h
from tools import data_gen, excelreader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    return render_template('index.html')

@app.route("/db_connection_test")
def db_connection_test():
    try:
        connection_uri = os.getenv("DATABASE_URL")
        print(connection_uri)
        conn = psycopg2.connect(connection_uri)
        conn.close()
    except Exception as e:
        print(e)

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

    sort = h.Hungarian(groups_dict, students_dict)
    sort.run()
    output_data = sort.get_data()

    return render_template("results.html", results1 = output_data.selections, happiness_data = output_data.happiness_data,
                           time = output_data.time, happiness = output_data.happiness)

@app.route("/excel")
def excel():
    groups_dict = excelreader.create_groups()
    students_dict = excelreader.create_users(groups_dict)

    sort = h.Hungarian(groups_dict, students_dict)
    sort.run()
    output_data = sort.get_data()

    return render_template("results.html", results = output_data.selections, happiness_data = output_data.happiness_data,
                           time = output_data.time, happiness = output_data.happiness)
