import unittest
import numpy as np
from src.entities.group import Group
from src.entities.student import Student
from src.algorithms.weights import Weights
from src.algorithms.hungarian import Hungarian
from copy import deepcopy

class TestHungarian(unittest.TestCase):
    def setUp(self):
        """
        Sets up a small number of groups and students with appropriate weights,
        inputs them to the hungarian algorithm and calls functions to run
        the algorithm while saving some of the preliminary data structures for tests
        """
        self.groups = {22:Group(22,'Ducks',2), 14:Group(14,'Geese',1), 55:Group(55,'Mallards',1), 19:Group(19, "Roided Harpy Eagles", 1)}
        self.students = {114:Student(114, 'Jane', [22,14,55], []),
                        367:Student(367, 'Joe', [22,55,14], []),
                        847:Student(847, 'Janet', [55,22,14], [])}
        self.weights = Weights(len(self.groups), len(self.students)).get_weights()
        self.h = Hungarian(self.groups, self.students, self.weights)
        self.original_matrix = self.h.matrix
        self.original_assigned_groups_dict = deepcopy(self.h.assigned_groups)
        self.original_student_happiness = self.h.student_happiness
        self.h.reshape_matrix()
        self.reshaped_matrix = self.h.matrix
        self.h.profit_matrix_to_cost_matrix()
        self.h.find_assignment()

    def test_students_saved(self):
        """
        Checks student names to see the students are saved correctly
        """
        names = [student.name for key, student in self.h.students.items()]
        self.assertEqual(names, ['Jane', 'Joe', 'Janet'])

    def test_groups_saved(self):
        """
        Checks group names to see the groups are saved correctly
        """
        names = [group.name for key, group in self.h.groups.items()]
        self.assertEqual(names, ['Ducks', 'Geese', 'Mallards', 'Roided Harpy Eagles'])

    def test_weights_saved(self):
        """
        Checks saved weights keys to see that keys neede by the algorithm are found
        """
        keys = [key for key, weight in self.h.weights.items()]
        self.assertEqual(keys, [0, 1, 2, 3, -1, None])

    def test_create_student_to_id_dict(self):
        """
        Tests that the dictionary mapping matrix indices to student IDs
        contains the correct student IDs
        """
        student_ids = [student for key, student in self.h.index_to_student_dict.items()]
        self.assertEqual(student_ids, [114,367,847])

    def test_create_group_to_id_dict(self):
        """
        Tests that the group dictionary mapping matrix indices to groups
        creates the correct dictionary by checking the list of group IDs
        """
        group_ids = [group for key,group in self.h.index_to_group_dict.items()]
        self.assertEqual(group_ids, [22, 22, 14, 55, 19])

    def test_initial_matrix_created_correctly(self):
        """
        Tests that matrix initially contains correct weights
        """
        np.testing.assert_array_equal(self.original_matrix,
                                      np.array([[18, 18, 15, 12, 6],
                                                [18, 18, 12, 15, 6],
                                                [15, 15, 12, 18, 6]]))

    def test_that_assigned_groups_dict_has_correct_number_of_groups_initially(self):
        """
        Tests that the length of the original dictionary is equal to the number of groups
        """
        self.assertEqual(len(self.original_assigned_groups_dict), len(self.h.groups))

    def test_that_initiated_assigned_groups_dict_contains_empty_lists(self):
        """"
        Makes sure that the original assigned groups dictionary is empty, so there are no
        group assignments prior to running the algorithm
        """
        self.assertEqual(sum([len(students) for key,students in self.original_assigned_groups_dict.items()]), 0)

    def test_that_initial_student_happiness_array_has_correct_dimensions(self):
        """
        Tests that array has as many rows as there's students and two columns
        """
        self.assertEqual(np.shape(self.original_student_happiness),(len(self.h.students), 2))

    def test_that_reshaped_matrix_is_nxn(self):
        """
        The algorithm needs and nxn algorithm, test that after matrix has been reshaped
        the matrix is square
        """
        x, y = np.shape(self.reshaped_matrix)
        self.assertEqual(x, y)

    def test_nxn_matrix_adds_empty_rows_to_bottom(self):
        """
        Test that empty rows in creating nxn matrix have been added to the bottom
        by checking that top part matches original matrix
        """
        np.testing.assert_array_equal(self.reshaped_matrix[0:3,], self.original_matrix)

    def tests_that_reshape_pads_with_correct_minimum_weight(self):
        """
        Checks that the number of unique values on the padded row is 1 and
        that it matches the empty weight (key -1) in the weights dictionary
        """
        values = np.unique(self.reshaped_matrix[-1])
        self.assertEqual((len(values),values[0]),(1,self.weights[-1]))

    def test_profit_to_cost_matrix_works_correctly(self):
        """
        Checks that row 0 col 0 value that was previously highest value is 0
        after hungarian function profit_matrix_to_cost_matrix and that the
        previously lowest value used for padding the matrix  is now
        the highest value in the matrix
        """
        max = np.max(self.h.matrix)
        self.assertEqual((self.h.matrix[0,0],self.h.matrix[2,4]),(0,max))

    def test_students_sorted_to_correct_groups(self):
        """
        Tests the simple case with only a few students and few groups
        to see that students are put in their favourite groups
        """
        assigned_groups = [students for key,students in self.h.assigned_groups.items()]
        self.assertEqual(assigned_groups, [[114, 367], [], [847], []])

    def tests_student_happiness_updated_after_group_assignment(self):
        """
        Tests that no student happiness score is 0 after assignment
        This group assinment should have all students in their first preference
        so test checks that all values are 1
        """
        values = np.unique(self.h.student_happiness[:,1])
        self.assertEqual((len(values),values[0]),(1,1))

    def test_algorithm_function_run_calls_correct_functions(self):
        """
        Tests that after reverting algo matrix to original matrix and calling run()
        the resulting algorithm is equal to the matrix resulting from manually calling
        appropriate functions in setUp
        """
        ref = self.h.matrix
        self.h.matrix = self.original_matrix
        self.h.run()
        np.testing.assert_array_equal(self.h.matrix,ref)

    def test_get_data_returns_correct_size_tuple(self):
        """
        Calls get data and tests that the tuple has 4 members
        """
        self.assertEqual(len(self.h.get_data()), 3)

    def test_get_happiness_data_strings_returns_correct_format(self):
        """
        Checks that function get_happiness_data_strings returns data in correct format
        """
        happiness = self.h.get_happiness_data_strings()
        self.assertEqual((len(happiness), happiness[0]),(1,'1. valintaansa sijoitetut opiskelijat: 3 kpl'))

    def test_reshape_matrix_can_add_empty_columns(self):
        """
        Adds students to the student pool until number of students is higher than number
        of spots available for students.
        Checks that last column has only one unique value that is equal to weights
        value for key -1
        """
        self.students[999] = Student(999, 'Bob', [22,14,55], [])
        self.students[654] = Student(654, "Ginny", [14,22,55], [])
        self.students[754] = Student(754, "Ronald", [55,22,14], [])
        weights = Weights(len(self.groups), len(self.students)).get_weights()
        h = Hungarian(self.groups, self.students, weights)
        h.reshape_matrix()
        values = np.unique(h.matrix[:,-1])
        self.assertEqual((len(values), values[0]),(1,weights[-1]))

    def test_that_reshape_does_not_add_columns_if_not_needed(self):
        """
        Adds one student so that available spots is equal to number of students
        and matrix should not be padded
        """
        self.students[999] = Student(999, 'Bob', [22,14,55], [])
        self.students[754] = Student(754, "Ronald", [55,22,14], [])
        weights = Weights(len(self.groups), len(self.students)).get_weights()
        h = Hungarian(self.groups, self.students, weights)
        ref = h.matrix
        h.reshape_matrix()
        np.testing.assert_array_equal(h.matrix, ref)

    def test_correct_matrix_with_rejections(self):
        """
        Add students with rejections and check that the matrix contains the correct values.
        """
        self.students[999] = Student(999, 'Bob', [19,14,22], [55])
        self.students[754] = Student(754, "Ronald", [55,22,14], [19])
        h = Hungarian(self.groups, self.students, self.weights)
        new_matrix = h.matrix
        np.testing.assert_array_equal(new_matrix,
                                      np.array([[18, 18, 15, 12, 6],
                                                [18, 18, 12, 15, 6],
                                                [15, 15, 12, 18, 6],
                                                [12, 12, 15, 0, 18],
                                                [15, 15, 12, 18, 0]]))

    def test_happiness_number_correct_fors_student_placed_outside_their_preference(self):
        """
        Adds students with identical choices and tests that for the student
        placed outside of their preference list the happiness score is
        number of choices + 1
        There's 5 students and 5 spaces but no student chose group with id 19
        so we find the student assigned to 19 and check that they are sufficiently
        not happy
        """
        self.students[334] = Student(334, 'Bob', [22,14,55], [])
        self.students[324] = Student(324, 'Ronald', [22,14,55], [])
        h = Hungarian(self.groups, self.students, self.weights)
        h.run()
        student = h.assigned_groups[19][0]
        happiness = int(h.student_happiness[h.student_happiness[:,0] == student][0][1])
        self.assertEqual(happiness, 5)