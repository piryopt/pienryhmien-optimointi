import unittest
import numpy as np
from src.entities.group import Group
from src.entities.student import Student
from src.algorithms.hungarian import Hungarian
from copy import deepcopy

class TestHungarian(unittest.TestCase):
    def setUp(self):
        """
        Sets up a small number of groups and students with trivial weights,
        inputs them to the hungarian algorithm and calls functions to run
        the algorithm and saves some of the data structures for tests
        """
        small_groups = {0:Group(0,'A',2), 1:Group(1,'B',1), 2:Group(2,'C',1)}
        few_students = {0:Student(0, 'A', [0,1,2]),
                        1:Student(1, 'B', [0,2,1]),
                        2:Student(2, 'C', [2,0,1])}
        small_weights = {0:20, 1:10, 2:0}
        self.h = Hungarian(small_groups, few_students, small_weights)
        self.original_matrix = self.h.matrix
        self.original_assigned_groups_dict = deepcopy(self.h.assigned_groups)
        self.original_student_happiness = self.h.student_happiness
        self.h.run()
        

    def test_create_group_dict(self):
        """
        Tests that the group dictionary mapping matrix indices to groups
        creates the correct dictionary by getting group id's by key
        into a list from index_to_group_dict
        """
        group_ids = [group for key,group in self.h.index_to_group_dict.items()]
        self.assertEqual(group_ids, [0, 0, 1, 2])

    def test_initial_matrix_created_correctly(self):
        """
        Tests that the matrix created matches the given groups and students before
        the step adding empty rows
        """
        np.testing.assert_array_equal(self.original_matrix,
                                      np.array([[20, 20, 10, 0],
                                                [20, 20, 0, 10],
                                                [10, 10, 0, 20]]))

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

    def test_that_matrix_is_nxn(self):
        """
        The algorithm needs and nxn algorithm, test that after matrix has been reshaped
        the matrix is square
        """
        x, y = np.shape(self.h.matrix)
        self.assertEqual(x, y)

    def test_nxn_matrix_adds_empty_rows_to_bottom(self):
        """
        Test that empty rows in creating nxn matrix have been added to the bottom

        Note! This test will break and need to be modified once algorithm is modified so
        that the empty value is not the highest to give the highest values to people who
        can't be placed in a certain group
        """
        self.assertEqual(sum(self.h.matrix[-1]), 80)

    def test_students_sorted_to_correct_groups(self):
        """
        Tests the simple case with only a few students and few groups
        to see that students are put in their favourite groups
        """
        assigned_groups = [students for key,students in self.h.assigned_groups.items()]
        self.assertEqual(assigned_groups, [[0,1], [], [2]])

    def test_get_data_returns_correct_size_tuple(self):
        """
        Calls get data and tests that the tuple has 4 members
        """
        self.assertEqual(len(self.h.get_data()), 4)

    def test_profit_matrix_to_cost_matrix(self):
        """
        Creates a new small instance of hungarian algorithm to test that
        the profit matrix to cost matrix works as intended
        """
        small_groups = {0:Group(0,'A',1), 1:Group(1,'B',1), 2:Group(2,'C',1)}
        few_students = {0:Student(0, 'A', [0,1,2]),
                        1:Student(1, 'B', [0,2,1]),
                        2:Student(2, 'C', [2,0,1])}
        small_weights = {0:20, 1:10, 2:0}
        h = Hungarian(small_groups, few_students, small_weights)
        h.profit_matrix_to_cost_matrix()
        np.testing.assert_array_equal(h.matrix, np.array([[0,10,20],[0,20,10],[10,20,0]]))

    def test_reshape_matrix_can_add_empty_columns(self):
        """
        Creates a small instance of hungarian algorithm to test that if the algorithm
        needs added columns to the matrix, they are empty
        """
        small_groups = {0:Group(0,'A',1), 1:Group(1,'B',1), 2:Group(2,'C',1)}
        few_students = {0:Student(0, 'A', [0,1,2]),
                        1:Student(1, 'B', [0,2,1]),
                        2:Student(2, 'C', [2,0,1]),
                        3:Student(3, 'C', [1,0,2])}
        small_weights = {0:20, 1:10, 2:0}
        h = Hungarian(small_groups, few_students, small_weights)
        h.reshape_matrix()
        np.testing.assert_array_equal(h.matrix, np.array([[20,10,0,0],
                                                          [20,0,10,0],
                                                          [10,0,20,0],
                                                          [10,20,0,0]]))
