import os

from flask import render_template, request
from app import app
from copy import deepcopy
import algorithms.hungarian as h
from entities.input_data import Input_data
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

    groups_dict = hospital_data_gen.generate_groups(group_n, max_group_size)
    students_dict = hospital_data_gen.generate_students(student_n, groups_dict)

    groups_dict2 = deepcopy(groups_dict)
    students_dict2 = deepcopy(students_dict)

    #groups_dict = excelreader.create_groups()
    #students_dict = excelreader.create_users(groups_dict)

    input_data = Input_data(groups_dict, students_dict, max_selections, max_group_size)
    sort = Hospital(input_data)
    output_data = sort.hospital_algo()

    sort2 = h.Hungarian(groups_dict2, students_dict2)
    sort2.run()
    output_data2 = sort2.get_data()

    return render_template("results.html", results1 = output_data.selections, happiness_data1 = output_data.happiness_data,
                           time1 = output_data.time, happiness1 = output_data.happiness, results2 = output_data2.selections,
                           happiness_data2 = output_data2.happiness_data, time2 = output_data2.time, happiness2 = output_data2.happiness)
