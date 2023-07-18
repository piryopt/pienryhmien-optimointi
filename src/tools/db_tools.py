from src import db
from sqlalchemy import text

def clear_database():
    db.session.execute(text("DELETE FROM final_group"))
    db.session.execute(text("DELETE FROM user_survey_rankings"))
    db.session.execute(text("DELETE FROM choice_infos"))
    db.session.execute(text("DELETE FROM survey_choices"))
    db.session.execute(text("DELETE FROM surveys"))
    db.session.execute(text("DELETE FROM users"))
    db.session.commit()