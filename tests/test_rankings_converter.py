import pytest
from src.tools.rankings_converter import convert_to_list, convert_to_string



@pytest.fixture
def ranking_data():
    ranking_string = "4,3,6,7,2,5"
    ranking_list = ["4", "3", "6", "7", "2", "5"]
    return {
        "ranking_string": ranking_string,
        "ranking_list": ranking_list
    }

def test_string_to_list(ranking_data):
    """
    Test that converting a string to a list works
    """
    new_list = convert_to_list(ranking_data["ranking_string"])
    assert new_list == ranking_data["ranking_list"]

def test_list_to_string(ranking_data):
    """
    Test that converting a list to a string works
    """
    new_string = convert_to_string(ranking_data["ranking_list"])
    assert new_string == ranking_data["ranking_string"]
