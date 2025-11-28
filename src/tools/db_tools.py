from sqlalchemy import text
from src import db
from random import randint


def clear_database():
    db.session.execute(text("DELETE FROM final_group"))
    db.session.execute(text("DELETE FROM user_survey_rankings"))
    db.session.execute(text("DELETE FROM choice_infos"))
    db.session.execute(text("DELETE FROM survey_choices"))
    db.session.execute(text("DELETE FROM survey_stages"))
    db.session.execute(text("DELETE FROM survey_owners"))
    db.session.execute(text("DELETE FROM surveys"))
    db.session.execute(text("DELETE FROM feedback"))
    db.session.execute(text("DELETE FROM users"))
    db.session.execute(text("DELETE FROM statistics"))
    db.session.commit()


def generate_unique_id(char_count):
    return "".join([generate_random_character() for _ in range(char_count)])


def generate_random_character():
    char_numbers = [*range(48, 58)] + [*range(65, 91)] + [*range(97, 123)]
    return chr(char_numbers[randint(0, len(char_numbers) - 1)])
