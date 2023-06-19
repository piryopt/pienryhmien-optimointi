import unittest
from src.algorithms.weights import Weights

class TestWeights(unittest.TestCase):
    def setUp(self):
        self.n_choices = 3
        self.n_students = 0
        self.w = Weights(self.n_choices, self.n_students, True)

    def test_weights_created(self):
        self.assertGreater(len(self.w.weights), 0)

    def test_correct_number_of_weights_created(self):
        self.assertEqual(len(self.w.weights), 4)

    def test_weight_values_are_correct(self):
        self.assertEqual(self.w.weights[0], self.n_students*self.n_choices)

    def test_function_get_weights_returns_something(self):
        self.assertGreater(len(self.w.get_weights()), 0)

    def test_function_get_weights_returns_correct_number_of_weights(self):
        self.assertEqual(len(self.w.get_weights()), 4)

    def test_correct_number_of_weights_created_when_min_in_choices_false(self):
        w = Weights(3,3,False)
        self.assertEqual(len(w.weights), 5)