import unittest
from src.algorithms.weights import Weights

class TestWeights(unittest.TestCase):
    """
    Tests class that creates weights for the hungarian algorithm.
    """

    def setUp(self):
        """
        Sets up a small number of weights in two ways
        1: Minimum weight is assigned to the lowest/last choice
        2: Minimum weight is assigned to groups not in choices, so one extra weight is needed
        """
        self.n_choices = 3
        self.n_students = 3
        self.w = Weights(self.n_choices, self.n_students)

    def test_weights_created(self):
        """
        Tests that after init the dictionary of weights has items in it
        """
        self.assertGreater(len(self.w.weights), 0)

    def test_correct_number_of_weights_created(self):
        """
        Test that number of items in dictionary includes all 3 choices specified
        in creating weights plus a Null weight when min_in_choices is True
        """
        self.assertEqual(len(self.w.weights), 5)

    def test_weight_values_are_correct(self):
        """
        Tests that the third highest weight number is correct. As it depends on
        both the highest weight, the weight interval and the checked number is not
        copypasted from the algorithm code directly, this is a reasonably good test
        that all weights should be correct
        """
        self.assertEqual(self.w.weights[2], self.n_students*self.n_choices)

    def test_function_get_weights_returns_something(self):
        """
        Tests that the class function get_weights returns an item with a
        length greater than 0, i.e. has a return
        """
        self.assertGreater(len(self.w.get_weights()), 0)

    def test_function_get_weights_returns_correct_number_of_weights(self):
        """
        Tests that the number of weights returned by get weights is correct
        """
        self.assertEqual(len(self.w.get_weights()), 5)

    def test_function_get_weights_returns_the_correct_dictionary(self):
        """
        Checks get_weights return against weights variable in the object
        """
        self.assertEqual(self.w.get_weights(), self.w.weights)
