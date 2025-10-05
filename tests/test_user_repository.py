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
