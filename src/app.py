from flask import Flask, render_template
from algorithms.hospital import hospital_algo
from tools import hospital_data_gen

app = Flask(__name__)

group_n = 500
student_n = 10000
max_group_size = 20
max_selections = 10
excel = 'Kohtitutkivaatyötapaa.xlsx'

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    groups_dict = hospital_data_gen.generate_groups(group_n)
    students_dict = hospital_data_gen.generate_students(student_n, groups_dict)

    hospital_algo(groups_dict, students_dict)

    return render_template('index.html')

