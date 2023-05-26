from flask import render_template, request
from app import app
from algorithms.hospital import hospital_algo
from tools import hospital_data_gen

group_n = 50
student_n = 1000
max_group_size = 20
max_selections = 10
excel = 'Kohtitutkivaatyötapaa.xlsx'

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    return render_template('index.html')

@app.route("/hospitalinput_test")
def hospitalinput_test() -> str:
    return render_template('hospitalinput_test.html')

@app.route("/hospital_test", methods = ["POST"])
def hospital_test() -> str:
    group_n = int(request.form.get("group_n"))
    student_n = int(request.form.get("student_n"))
    max_group_size = int(request.form.get("max_group_size"))
    max_selections = int(request.form.get("max_selections"))

    groups_dict = hospital_data_gen.generate_groups(group_n)
    students_dict = hospital_data_gen.generate_students(student_n, groups_dict)

    data = hospital_algo(groups_dict, students_dict, max_selections, max_group_size)
    return render_template("hospital_test.html", groups_dict=data[0], students_dict = students_dict, time = data[1], happiness = data[2])
