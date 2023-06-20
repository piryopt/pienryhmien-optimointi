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
        self.n_students = 0
        self.w1 = Weights(self.n_choices, self.n_students, min_in_choices=True)
        self.w2 = Weights(self.n_choices, self.n_students, min_in_choices=False)

    def test_weights_created(self):
        """
        Tests that after init the dictionary of weights has items in it
        """
        self.assertGreater(len(self.w1.weights), 0)

    def test_correct_number_of_weights_created(self):
        """
        Test that number of items in dictionary includes all 3 choices specified
        in creating weights plus a Null weight when min_in_choices is True
        """
        self.assertEqual(len(self.w1.weights), 4)

    def test_correct_number_of_weights_created_when_min_in_choices_false(self):
        """
        Tests that the number of weights created with min_in_choices False is
        one more than when it is True
        """
        self.assertEqual(len(self.w2.weights), 5)

    def test_weight_values_are_correct(self):
        """
        Tests that the highest weight number is correct. As each weight depends on
        the one below it and the highest should be number of students multiplied
        by numer of choices, this is a reasonably good test that all weights
        are correct
        """
        self.assertEqual(self.w1.weights[0], self.n_students*self.n_choices)

    def test_weight_values_are_correct_when_min_in_choices_false(self):
        """
        Tests that when in addition to choices a separate min value is needed
        the highest weight is the number of students multiplied by 1 + number of
        choices
        """
        self.assertEqual(self.w2.weights[0], self.n_students*(1+self.n_choices))

    def test_function_get_weights_returns_something(self):
        """
        Tests that the class function get_weights returns an item with a
        length greater than 0, i.e. has a return
        """
        self.assertGreater(len(self.w1.get_weights()), 0)

    def test_function_get_weights_returns_correct_number_of_weights(self):
        """
        Tests that the number of weights returned by get weights is correct
        """
        self.assertEqual(len(self.w1.get_weights()), 4)
