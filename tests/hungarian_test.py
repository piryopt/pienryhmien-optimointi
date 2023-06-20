import unittest
import numpy as np
from src.entities.group import Group
from src.entities.student import Student
from src.algorithms.hungarian import Hungarian

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
        self.original_assigned_groups_dict = self.h.assigned_groups
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

    def test_matrix_created_correctly(self):
        """
        Tests that the matrix created matches the given groups and students before
        the step adding empty rows
        """
        np.testing.assert_array_equal(self.original_matrix,
                                      np.array([[20, 20, 10, 0],
                                                [20, 20, 0, 10],
                                                [10, 10, 0, 20]]))

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
