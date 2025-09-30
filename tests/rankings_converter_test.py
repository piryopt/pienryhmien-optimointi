import unittest
from src.tools.rankings_converter import convert_to_list, convert_to_string


class TestWeights(unittest.TestCase):
    def setUp(self):
        self.ranking_string = "4,3,6,7,2,5"
        self.ranking_list = ["4", "3", "6", "7", "2", "5"]

    def test_string_to_list(self):
        """
        Test that converting a string to a list works
        """
        new_list = convert_to_list(self.ranking_string)
        self.assertEqual(new_list, self.ranking_list)

    def test_list_to_string(self):
        """
        Test that converting a list to a string works
        """
        new_string = convert_to_string(self.ranking_list)
        self.assertEqual(new_string, self.ranking_string)
