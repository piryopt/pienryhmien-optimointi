from src.repositories.user_repository import user_repository as ur


def test_get_user_by_email_invalid(setup_db):
    """
    Test that an invalid email returns False
    """
    user = ur.get_user_by_email("moti@motivaatio.com")
    assert not user


def test_get_user_by_email(setup_db):
    """
    Test that a user is returned with the correct email
    """
    user = ur.get_user_by_email("tiina.testiope@email.com")
    assert user.name == "Tiina Testiopettaja"
    assert user.email == "tiina.testiope@email.com"
    assert user.isteacher


def test_get_user_data_returns_false_for_invalid_id(test_app):
    """
    Test that get_user_data() returns False if user not found or id invalid
    """

    incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, []]
    for item in incorrect_ids:
        assert ur.get_user_data(item) is False


def test_change_user_language_returns_false_for_invalid_user_id(test_app):
    """
    Test that changing language with an invalid user id returns False
    """
    incorrect_ids = ["x", "kukkuluuruu", 3.14, "55", False, True, []]
    for item in incorrect_ids:
        assert ur.change_user_language(item, "en") is False
