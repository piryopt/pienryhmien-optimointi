import os

from flask import render_template, request
from app import app
from algorithms.hospital import Hospital
from entities.input_data import Input_data
from tools import hospital_data_gen, excelreader
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_urls import DatabaseURL
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

@app.route("/hospitalinput_test")
def hospitalinput_test() -> str:
    return render_template('hospitalinput_test.html')

@app.route("/results", methods = ["POST"])
def results():    
    group_n = int(request.form.get("group_n"))
    student_n = int(request.form.get("student_n"))
    max_group_size = int(request.form.get("max_group_size"))
    max_selections = int(request.form.get("max_selections"))

    groups_dict = hospital_data_gen.generate_groups(group_n)
    students_dict = hospital_data_gen.generate_students(student_n, groups_dict)

    #groups_dict = excelreader.create_groups()
    #students_dict = excelreader.create_users(groups_dict)

    input_data = Input_data(groups_dict, students_dict, max_selections, max_group_size)
    sort = Hospital(input_data)
    output_data = sort.hospital_algo()

    return render_template("results.html", results = output_data.selections, happiness_data = output_data.happiness_data,
                           time = output_data.time, happiness = output_data.happiness)
