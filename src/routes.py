from flask import render_template, request
from app import app
from algorithms.hospital import Hospital
from entities.input_data import Input_data
from tools import hospital_data_gen, excelreader

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

    #groups_dict = excelreader.create_groups()
    #students_dict = excelreader.create_users(groups_dict)

    input_data = Input_data(groups_dict, students_dict, max_selections, max_group_size)
    sort = Hospital(input_data)
    output_data = sort.hospital_algo()
    return render_template("hospital_test.html", groups_dict=output_data.groups_dict, students_dict = students_dict, time = output_data.time, happiness = output_data.happiness)
