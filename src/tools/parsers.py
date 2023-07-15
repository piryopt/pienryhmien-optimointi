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

def parser_elomake_csv(file, survey_name, user_id):
    '''
    Parses a survey from Elomake exported CSV file and creates a survey,
    including choices etc.
    The last column on a row (probably) contains unprintable control characters,
    which is why straight up strip() doesn't work, so they have to removed at all
    points that could be the last column.
    '''
    survey_id = survey_repository.create_new_survey(survey_name, user_id)

    file = file.split('\n')
    row_count = len(file)
    info_headers = []
    first_row = file[0].split('''","''')
    col_count = len(first_row)

    # add column headers to own array
    for cell in first_row:
        # remove unseen control characters etc.
        temp = ''.join(c for c in cell if c.isprintable())
        # remove leftover " from parsing
        info_headers.append(temp.strip('"'))

    index = 0
    for line in file:
        # bad, but using file[index] doesn't work
        if index == row_count - 1:
            break
        if index == 0:
            index += 1
            continue

        temp = line.split('''","''')
        name = ''.join(c for c in temp[2] if c.isprintable())
        spaces = ''.join(c for c in temp[3] if c.isprintable()).strip('"')

        choice_id = survey_repository.create_new_survey_choice(survey_id, name, int(spaces))

        i = 4
        while i < col_count:
            temp_string = ''.join(c for c in temp[i] if c.isprintable())
            survey_repository.create_new_choice_info(choice_id, info_headers[i], temp_string.strip('"'))
            i += 1

        index += 1

