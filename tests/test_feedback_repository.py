import pytest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.feedback_repository import feedback_repository as fr
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database




@pytest.fixture(autouse=True)
def setup_env():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    db.init_app(app)

    app_context = app.app_context()
    app_context.push()

    clear_database()

    user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
    ur.register(user1)
    user_id = ur.find_by_email(user1.email)[0]

    yield {
        "app": app,
        "app_context": app_context,
        "user_id": user_id,
    }

    db.session.remove()
    db.drop_all()
    app_context.pop()



def test_new_feedback(setup_env):
    """
    Test that creating new feedback works
    """
    d = setup_env
    success = fr.new_feedback(d["user_id"], "Testi palaute 1", "bugi", "Toimiiko eka testi?")
    assert success

def test_get_feedbacK(setup_env):
    """
    Test that getting a valid feedback works
    """
    d = setup_env
    feedback_id = ""
    fr.new_feedback(d["user_id"], "Testi palaute 2", "bugi", "Toimiiko toka testi?")
    feedback_list = fr.get_unsolved_feedback()
    for f in feedback_list:
        if f.title == "Testi palaute 2":
            feedback_id = f.id
    feedback = fr.get_feedback(feedback_id)
    assert feedback.title == "Testi palaute 2"

def test_get_invalid_feedbacK():
    """
    Test that getting a invalid feedback works
    """
    success = fr.get_feedback(-1)
    assert not success

def test_get_unsolved_feedback(setup_env):
    """
    Test that the list of unsolved feedback is the correct size
    """
    d = setup_env
    fr.new_feedback(d["user_id"], "Testi palaute 5", "bugi", "Toimiiko 5. testi?")
    unsolved_list = fr.get_unsolved_feedback()
    assert len(unsolved_list) == 1

def test_mark_feedback_solved(setup_env):
    """
    Test that closing a feedback works and that the list of solved feedback is the correct size
    """
    d = setup_env
    fr.new_feedback(d["user_id"], "Testi palaute 3", "bugi", "Toimiiko kolmas testi?")
    feedback_id = ""
    feedback_list = fr.get_unsolved_feedback()
    for f in feedback_list:
        if f.title == "Testi palaute 3":
            feedback_id = f.id
    success = fr.mark_feedback_solved(feedback_id)
    assert success
    feedback = fr.get_feedback(feedback_id)
    assert feedback.solved
    unsolved_list = fr.get_solved_feedback()
    assert len(unsolved_list) == 1

def test_check_unsolved_title_doesnt_exist(setup_env):
    d = setup_env
    success = fr.check_unsolved_title_doesnt_exist(d["user_id"], "Testi palaute 4")
    assert success
    fr.new_feedback(d["user_id"], "Testi palaute 4", "bugi", "Toimiiko 4. testi?")
    success = fr.check_unsolved_title_doesnt_exist(d["user_id"], "Testi palaute 4")
    assert not success

def test_exceptions_false():
    """
    Test that all exceptions return False
    """
    success = fr.new_feedback(-1, "Testi palaute 3", "bugi", "Toimiiko kolmas testi?")
    assert not success
    success = fr.get_feedback(-1)
    assert not success
    success = fr.check_unsolved_title_doesnt_exist(-1, "Motivaatio")
    assert not success
    success = fr.mark_feedback_solved(-1)
    assert not success
