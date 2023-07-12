import csv
from src import db
from src.repositories.survey_repository import survey_repository
from sqlalchemy import text

def clear_database():
    db.session.execute(text("DELETE FROM final_group"))
    db.session.execute(text("DELETE FROM user_survey_rankings"))
    db.session.execute(text("DELETE FROM choice_infos"))
    db.session.execute(text("DELETE FROM survey_choices"))
    db.session.execute(text("DELETE FROM surveys"))
    db.session.execute(text("DELETE FROM users"))
    db.session.commit()


def parser_elomake_csv(filename, survey_name, teacher_id): # bit verbose, but should be easy to read
    '''
    Parses a survey from Elomake exported CSV file and creates a survey,
    including choices etc.
    '''
    survey_id = survey_repository.create_new_survey(survey_name, teacher_id)

    filename = "documentation/" + filename

    with open(filename, "r") as file:
        reader = csv.reader(file, delimiter=",")

        temp = next(reader)
        temp_length = len(temp)
        keys = []
        i = 0
        while i < temp_length:
            keys.append(temp[i])
            i += 1


        for row in reader: # dynamic amount of additional infos

            row_length = len(row)

            name = row[2]
            max_spaces = int(row[3])

            choice_id = survey_repository.create_new_survey_choice(survey_id, name, max_spaces)

            i = 4
            while i < row_length:
                key = temp[i]
                value = row[i]
                i += 1

                survey_repository.create_new_choice_info(choice_id, key, value)

                # add to choice_infos here
