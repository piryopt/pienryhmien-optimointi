import unittest
import numpy as np
from src.entities.group import Group
from src.entities.student import Student
from src.algorithms.hungarian import Hungarian

class TestHungarian(unittest.TestCase):
    def setUp(self):
        small_groups = {0:Group(0,'A',1), 1:Group(1,'B',1), 2:Group(2,'C',1)}
        few_students = {0:Student(0, 'A', [0,1,2]), 1:Student(1, 'B', [0,2,1]), 2:Student(2, 'C', [2,0,1])}
        small_weights = {0:20, 1:10, 2:0}
        self.h = Hungarian(small_groups, few_students, small_weights)

    def test_matrix_created_correctly(self):
        self.h.create_group_dict()
        self.h.create_matrix()
        np.testing.assert_array_equal(self.h.matrix, np.array([[20, 10, 0], [20, 0, 10], [10, 0, 20]]))