import pytest
import os
import numpy as np
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.entities.group import Group
from src.entities.student import Student
from src.algorithms.weights import Weights
from src.algorithms.hungarian import Hungarian
from copy import deepcopy



@pytest.fixture(autouse=True)
def setup_env():
    """
    Sets up a small number of groups and students with appropriate weights,
    inputs them to the hungarian algorithm and calls functions to run
    the algorithm while saving some of the preliminary data structures for tests
    """
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    app.config["BABEL_DEFAULT_LOCALE"] = "fi"

    babel = Babel(app)
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()
    groups = {
        22: Group(22, "Ducks", 2, 0, False),
        14: Group(14, "Geese", 1, 0, False),
        55: Group(55, "Mallards", 1, 0, False),
        19: Group(19, "Roided Harpy Eagles", 1, 0, False),
    }
    students = {
        114: Student(114, "Jane", [22, 14, 55], []),
        367: Student(367, "Joe", [22, 55, 14], []),
        847: Student(847, "Janet", [55, 22, 14], []),
    }
    weights = Weights(len(groups), len(students)).get_weights()
    h = Hungarian(groups, students, weights)
    original_matrix = h.matrix
    original_assigned_groups_dict = deepcopy(h.assigned_groups)
    original_student_happiness = h.student_happiness
    h.reshape_matrix()
    reshaped_matrix = h.matrix
    h.profit_matrix_to_cost_matrix()
    h.find_assignment()

    yield {
        "app": app,
        "app_context": app_context,
        "groups": groups,
        "students": students,
        "weights": weights,
        "h": h,
        "original_matrix": original_matrix,
        "original_assigned_groups_dict": original_assigned_groups_dict,
        "original_student_happiness": original_student_happiness,
        "reshaped_matrix": reshaped_matrix,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()

def test_students_saved(setup_env):
    """
    Checks student names to see the students are saved correctly
    """
    h = setup_env["h"]
    names = [student.name for key, student in h.students.items()]
    assert names == ["Jane", "Joe", "Janet"]

def test_groups_saved(setup_env):
    """
    Checks group names to see the groups are saved correctly
    """
    h = setup_env["h"]
    names = [group.name for key, group in h.groups.items()]
    assert names == ["Ducks", "Geese", "Mallards", "Roided Harpy Eagles"]

def test_weights_saved(setup_env):
    """
    Checks saved weights keys to see that keys neede by the algorithm are found
    """
    h = setup_env["h"]
    keys = [key for key, weight in h.weights.items()]
    assert keys == [0, 1, 2, 3, -1, None]

def test_create_student_to_id_dict(setup_env):
    """
    Tests that the dictionary mapping matrix indices to student IDs
    contains the correct student IDs
    """
    h = setup_env["h"]
    student_ids = [student for key, student in h.index_to_student_dict.items()]
    assert student_ids == [114, 367, 847]

def test_create_group_to_id_dict(setup_env):
    """
    Tests that the group dictionary mapping matrix indices to groups
    creates the correct dictionary by checking the list of group IDs
    """
    h = setup_env["h"]
    group_ids = [group for key, group in h.index_to_group_dict.items()]
    assert group_ids == [22, 22, 14, 55, 19]

def test_initial_matrix_created_correctly(setup_env):
    """
    Tests that matrix initially contains correct weights
    """
    original_matrix = setup_env["original_matrix"]
    np.testing.assert_array_equal(original_matrix, np.array([[18, 18, 15, 12, 6], [18, 18, 12, 15, 6], [15, 15, 12, 18, 6]]))

def test_that_assigned_groups_dict_has_correct_number_of_groups_initially(setup_env):
    """
    Tests that the length of the original dictionary is equal to the number of groups
    """
    h = setup_env["h"]
    original_assigned_groups_dict = setup_env["original_assigned_groups_dict"]
    assert len(original_assigned_groups_dict) == len(h.groups)

def test_that_initiated_assigned_groups_dict_contains_empty_lists(setup_env):
    """
    Makes sure that the original assigned groups dictionary is empty, so there are no
    group assignments prior to running the algorithm
    """
    original_assigned_groups_dict = setup_env["original_assigned_groups_dict"]
    assert sum([len(students) for key, students in original_assigned_groups_dict.items()]) == 0

def test_that_initial_student_happiness_array_has_correct_dimensions(setup_env):
    """
    Tests that array has as many rows as there's students and two columns
    """
    h = setup_env["h"]
    original_student_happiness = setup_env["original_student_happiness"]
    assert np.shape(original_student_happiness) == (len(h.students), 2)

def test_that_reshaped_matrix_is_nxn(setup_env):
    """
    The algorithm needs and nxn algorithm, test that after matrix has been reshaped
    the matrix is square
    """
    reshaped_matrix = setup_env["reshaped_matrix"]
    x, y = np.shape(reshaped_matrix)
    assert x == y

def test_nxn_matrix_adds_empty_rows_to_bottom(setup_env):
    """
    Test that empty rows in creating nxn matrix have been added to the bottom
    by checking that top part matches original matrix
    """
    reshaped_matrix = setup_env["reshaped_matrix"]
    original_matrix = setup_env["original_matrix"]
    np.testing.assert_array_equal(reshaped_matrix[0:3,], original_matrix)

def tests_that_reshape_pads_with_correct_minimum_weight(setup_env):
    """
    Checks that the number of unique values on the padded row is 1 and
    that it matches the empty weight (key -1) in the weights dictionary
    """
    reshaped_matrix = setup_env["reshaped_matrix"]
    weights = setup_env["weights"]
    values = np.unique(reshaped_matrix[-1])
    assert (len(values), values[0]) == (1, weights[-1])

def test_profit_to_cost_matrix_works_correctly(setup_env):
    """
    Checks that row 0 col 0 value that was previously highest value is 0
    after hungarian function profit_matrix_to_cost_matrix and that the
    previously lowest value used for padding the matrix  is now
    the highest value in the matrix
    """
    h = setup_env["h"]
    max_val = np.max(h.matrix)
    assert (h.matrix[0, 0], h.matrix[2, 4]) == (0, max_val)

def test_students_sorted_to_correct_groups(setup_env):
    """
    Tests the simple case with only a few students and few groups
    to see that students are put in their favourite groups
    """
    h = setup_env["h"]
    assigned_groups = [students for key, students in h.assigned_groups.items()]
    assert assigned_groups == [[114, 367], [], [847], []]

def tests_student_happiness_updated_after_group_assignment(setup_env):
    """
    Tests that no student happiness score is 0 after assignment
    This group assinment should have all students in their first preference
    so test checks that all values are 1
    """
    h = setup_env["h"]
    values = np.unique(h.student_happiness[:, 1])
    assert (len(values), values[0]) == (1, 1)

def test_algorithm_function_run_calls_correct_functions(setup_env):
    """
    Tests that after reverting algo matrix to original matrix and calling run()
    the resulting algorithm is equal to the matrix resulting from manually calling
    appropriate functions in setUp
    """
    h = setup_env["h"]
    original_matrix = setup_env["original_matrix"]
    ref = h.matrix
    h.matrix = original_matrix
    h.run()
    np.testing.assert_array_equal(h.matrix, ref)

def test_get_happiness_data_strings_returns_correct_format(setup_env):
    """
    Checks that function get_happiness_data_strings returns data in correct format
    """
    h = setup_env["h"]
    happiness = h.get_happiness_data_strings()
    assert (len(happiness), happiness[0]) == (1, "1. valintaansa sijoitetut käyttäjät: 3")

def test_reshape_matrix_can_add_empty_columns(setup_env):
    """
    Adds students to the student pool until number of students is higher than number
    of spots available for students.
    Checks that last column has only one unique value that is equal to weights
    value for key -1
    """
    groups = setup_env["groups"]
    students = setup_env["students"]
    students[999] = Student(999, "Bob", [22, 14, 55], [])
    students[654] = Student(654, "Ginny", [14, 22, 55], [])
    students[754] = Student(754, "Ronald", [55, 22, 14], [])
    weights = Weights(len(groups), len(students)).get_weights()
    h = Hungarian(groups, students, weights)
    h.reshape_matrix()
    values = np.unique(h.matrix[:, -1])
    assert (len(values), values[0]) == (1, weights[-1])

def test_that_reshape_does_not_add_columns_if_not_needed(setup_env):
    """
    Adds one student so that available spots is equal to number of students
    and matrix should not be padded
    """
    groups = setup_env["groups"]
    students = setup_env["students"]
    students[999] = Student(999, "Bob", [22, 14, 55], [])
    students[754] = Student(754, "Ronald", [55, 22, 14], [])
    weights = Weights(len(groups), len(students)).get_weights()
    h = Hungarian(groups, students, weights)
    ref = h.matrix
    h.reshape_matrix()
    np.testing.assert_array_equal(h.matrix, ref)

def test_correct_matrix_with_rejections(setup_env):
    """
    Add students with rejections and check that the matrix contains the correct values.
    """
    groups = setup_env["groups"]
    students = setup_env["students"]
    weights = setup_env["weights"]
    students[999] = Student(999, "Bob", [19, 14, 22], [55])
    students[754] = Student(754, "Ronald", [55, 22, 14], [19])
    h = Hungarian(groups, students, weights)
    new_matrix = h.matrix
    np.testing.assert_array_equal(
        new_matrix, np.array([[18, 18, 15, 12, 6], [18, 18, 12, 15, 6], [15, 15, 12, 18, 6], [12, 12, 15, 0, 18], [15, 15, 12, 18, 0]])
    )

def test_happiness_number_correct_fors_student_placed_outside_their_preference(setup_env):
    """
    Adds students with identical choices and tests that for the student
    placed outside of their preference list the happiness score is
    number of choices + 1
    There's 5 students and 5 spaces but no student chose group with id 19
    so we find the student assigned to 19 and check that they are sufficiently
    not happy
    """
    groups = setup_env["groups"]
    students = setup_env["students"]
    weights = setup_env["weights"]
    students[334] = Student(334, "Bob", [22, 14, 55], [])
    students[324] = Student(324, "Ronald", [22, 14, 55], [])
    h = Hungarian(groups, students, weights)
    h.run()
    student = h.assigned_groups[19][0]
    happiness = int(h.student_happiness[h.student_happiness[:, 0] == student][0][1])
    assert happiness == 5
