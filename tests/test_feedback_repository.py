from src.repositories.feedback_repository import feedback_repository as fr


def test_new_feedback(setup_db):
    """
    Test that creating new feedback works
    """
    d = setup_db
    success = fr.new_feedback(d["user_id"], "Testi palaute 1", "bugi", "Toimiiko eka testi?")
    assert success


def test_get_feedback(setup_db):
    """
    Test that getting a valid feedback works
    """
    d = setup_db
    feedback_id = ""
    fr.new_feedback(d["user_id"], "Testi palaute 2", "bugi", "Toimiiko toka testi?")
    feedback_list = fr.get_feedback_by_solved(False)
    for f in feedback_list:
        if f.title == "Testi palaute 2":
            feedback_id = f.id
    feedback = fr.get_feedback(feedback_id)
    assert feedback.title == "Testi palaute 2"


def test_get_invalid_feedback():
    """
    Test that getting a invalid feedback works
    """
    success = fr.get_feedback(-1)
    assert not success


def test_get_unsolved_feedback(setup_db):
    """
    Test that the list of unsolved feedback is the correct size
    """
    d = setup_db
    fr.new_feedback(d["user_id"], "Testi palaute 5", "bugi", "Toimiiko 5. testi?")
    unsolved_list = fr.get_feedback_by_solved(False)
    assert len(unsolved_list) == 1


def test_mark_feedback_solved(setup_db):
    """
    Test that closing a feedback works and that the list of solved feedback is the correct size
    """
    d = setup_db
    fr.new_feedback(d["user_id"], "Testi palaute 3", "bugi", "Toimiiko kolmas testi?")
    feedback_id = ""
    feedback_list = fr.get_feedback_by_solved(False)
    for f in feedback_list:
        if f.title == "Testi palaute 3":
            feedback_id = f.id
    success = fr.mark_feedback_solved(feedback_id)
    assert success
    feedback = fr.get_feedback(feedback_id)
    assert feedback.solved
    unsolved_list = fr.get_feedback_by_solved(True)
    assert len(unsolved_list) == 1


def test_check_unsolved_title_doesnt_exist(setup_db):
    d = setup_db
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
