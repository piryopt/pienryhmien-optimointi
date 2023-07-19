from src import db
from src.repositories.survey_repository import survey_repository
from src.repositories.survey_choices_repository import survey_choices_repository
from sqlalchemy import text
import json

def parser_elomake_csv(file, survey_name, user_id, description):
    '''
    Parses a survey from Elomake exported CSV file and creates a survey,
    including choices etc.
    The last column on a row (probably) contains unprintable control characters,
    which is why straight up strip() doesn't work, so they have to removed at all
    points that could be the last column.
    '''
    survey_id = survey_repository.create_new_survey(survey_name, user_id, 1, description)

    ret_dict = {}
    ret_dict["surveyName"] = survey_name
    ret_dict["surveyDescription"] = description
    ret_dict["choices"] = [] # array of dicts

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

        # update dict/JSON
        ret_dict["choices"].append({})
        ret_dict["choices"][index - 1]["name"] = name
        ret_dict["choices"][index - 1]["spaces"] = spaces


        choice_id = survey_choices_repository.create_new_survey_choice(survey_id, name, int(spaces))

        i = 4
        while i < col_count:
            temp_string = ''.join(c for c in temp[i] if c.isprintable())
            survey_choices_repository.create_new_choice_info(choice_id, info_headers[i], temp_string.strip('"'))
            # update dict/JSON
            ret_dict["choices"][index - 1][info_headers[i]] = temp_string.strip('"')
            i += 1

        index += 1

    print(ret_dict)
    return survey_id


def parser_manual(survey_choices, survey_name, user_id, description):

    survey_id = survey_repository.create_new_survey(survey_name, user_id, 1, description)

    for choice in survey_choices:

        # unsophisticated, but since all the data is key-value pairs,
        # this is the way it has to be
        count = 0
        choice_id = 0
        for pair in choice:
            if count == 0:
                name = choice[pair]
                count += 1
                continue
            if count == 1:
                spaces = choice[pair]
                count += 1
                choice_id = survey_choices_repository.create_new_survey_choice(survey_id, name, spaces)
                continue

            survey_choices_repository.create_new_choice_info(choice_id, pair, choice[pair])
            count += 1

    return survey_id
