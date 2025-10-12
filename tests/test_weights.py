import pytest
from src.algorithms.weights import Weights


@pytest.fixture
def weights_obj():
    """
    Sets up a small number of weights in two ways
    1: Minimum weight is assigned to the lowest/last choice
    2: Minimum weight is assigned to groups not in choices, so one extra weight is needed
    """
    n_choices = 3
    n_students = 3
    w = Weights(n_choices, n_students)
    return w, n_choices, n_students


def test_weights_created(weights_obj):
    """
    Tests that after init the dictionary of weights has items in it
    """
    w, _, _ = weights_obj
    assert len(w.weights) > 0


def test_correct_number_of_weights_created(weights_obj):
    """
    Test that number of items in dictionary includes all 3 choices specified
    in creating weights plus a Null weight when min_in_choices is True
    """

    w, _, _ = weights_obj
    assert len(w.weights) == 5


def test_weight_values_are_correct(weights_obj):
    """
    Tests that the third highest weight number is correct. As it depends on
    both the highest weight, the weight interval and the checked number is not
    copypasted from the algorithm code directly, this is a reasonably good test
    that all weights should be correct
    """
    w, n_choices, n_students = weights_obj
    assert w.weights[2] == n_students * n_choices


def test_function_get_weights_returns_something(weights_obj):
    """
    Tests that the class function get_weights returns an item with a
    length greater than 0, i.e. has a return
    """
    w, _, _ = weights_obj
    assert len(w.get_weights()) > 0


def test_function_get_weights_returns_correct_number_of_weights(weights_obj):
    """
    Tests that the number of weights returned by get weights is correct
    """
    w, _, _ = weights_obj
    assert len(w.get_weights()) == 5


def test_function_get_weights_returns_the_correct_dictionary(weights_obj):
    """
    Checks get_weights return against weights variable in the object
    """
    w, _, _ = weights_obj
    assert w.get_weights() == w.weights
