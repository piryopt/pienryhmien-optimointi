import pytest
import os
from flask import Flask
from flask_babel import Babel
from dotenv import load_dotenv
from src import db
from src.services.feedback_service import feedback_service as fs
from src.repositories.user_repository import user_repository as ur
from src.repositories.feedback_repository import feedback_repository as fr
from src.entities.user import User
from src.tools.db_tools import clear_database



@pytest.fixture(autouse=True)
def setup_env():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    app.config["BABEL_DEFAULT_LOCALE"] = "fi"

    babel = Babel(app)
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()

    clear_database()

    user = User("Not on tren Testerr", "tren4lyfe@tester.com", True)
    ur.register(user)
    user_id = ur.find_by_email(user.email)[0]
    data = {
        "title": "Valitus testeistä",
        "type": "muu",
        "content": "Testikattavuus voisi olla parempi"
    }

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
        "data": data,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()



def test_new_feedback(setup_env):
    """
    Test that adding a new feedback works
    """
    d = setup_env
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert success

def test_new_feedback_title_exists(setup_env):
    """
    Test that you cannot add a feedback if the title exists
    """
    d = setup_env
    d["data"]["title"] = "otsikko"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert success
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert message == "Olet jo luonut palautteen tällä otsikolla!"

def test_new_feedback_content_too_short(setup_env):
    """
    Test that you cannot add feedback if the content is to short
    """
    d = setup_env
    d["data"]["title"] = "Valitus testeistä"
    d["data"]["content"] = "moti"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert not success
    assert message == "Sisältö on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 5."

def test_new_feedback_title_too_short(setup_env):
    """
    Test that you cannot add feedback if the title is to short
    """
    d = setup_env
    d["data"]["title"] = "aa"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert not success
    assert message == "Otsikko on liian lyhyt! Merkkimäärän täytyy olla suurempi kuin 3."

def test_unsolved_list(setup_env):
    """
    Test that the list of unsolved feedback is the correct size
    """
    d = setup_env
    d["data"]["title"] = "aaaaaaaaaa"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert success
    d["data"]["title"] = "bbbbbbbbbb"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert success
    feedback_list = fs.get_unsolved_feedback()
    assert len(feedback_list) == 2

def test_title_too_long(setup_env):
    """
    Test that the title of a new feedback isn't too long
    """
    d = setup_env
    d["data"]["title"] = "a" * 51
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert not success

def test_content_too_long(setup_env):
    """
    Test that the content of a new feedback isn't too long
    """
    d = setup_env
    d["data"]["title"] = "Valitus testeistä"
    d["data"]["content"] = "testit ovat heikkoja! " * 100
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert not success

def test_get_invalid_feedback():
    """
    Test that you cannot get an invalid feedback that hasn't been solved
    """
    success = fs.get_feedback(-1)
    assert not success

def test_get_feedback(setup_env):
    """
    Test that the data of an unsolved feedback is correct
    """
    d = setup_env
    d["data"]["title"] = "Testit ovat mahtavia!"
    d["data"]["content"] = "Huijasin, ne ovat heikkoja >:D"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert success
    all_unsolved_feedback = fr.get_unsolved_feedback()
    feedback = all_unsolved_feedback[-1]
    feedback_data = fs.get_feedback(feedback.id)
    assert feedback_data[1] == "Testit ovat mahtavia!"
    assert feedback_data[4] == "Huijasin, ne ovat heikkoja >:D"

def test_get_invalid_solved_feedback():
    """
    Test that you cannot get an invalid feedback that has been solved
    """
    solved_feedback = fs.get_solved_feedback()
    assert len(solved_feedback) == 0

def test_get_solved_feedback(setup_env):
    """
    Test that the data of a solved feedback is correct
    """
    d = setup_env
    d["data"]["title"] = "Testit ovat todella mahtavia!"
    d["data"]["content"] = "Huijasin, ne ovat heikkoja >:D"
    success, message = fs.new_feedback(d["user_id"], d["data"])
    assert success
    all_unsolved_feedback = fr.get_unsolved_feedback()
    feedback = all_unsolved_feedback[-1]
    fs.mark_feedback_solved(feedback.id)
    all_solved_feedback = fs.get_solved_feedback()
    feedback_data = all_solved_feedback[-1]
    assert feedback_data[1] == "Testit ovat todella mahtavia!"
