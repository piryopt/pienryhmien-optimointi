from src import db
from src.repositories.survey_repository import survey_repository
from src.repositories.survey_choices_repository import survey_choices_repository
from sqlalchemy import text

def parser_elomake_csv_to_dict(file):
    '''
    Parses an Elomake imported CSV to a dictionary,
    the dictionary is later used by parser_manual() (below)
    RETURNS dictionary that can be parsed by later functions
    '''

    ret_dict = {}
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

        i = 4
        while i < col_count:
            temp_string = ''.join(c for c in temp[i] if c.isprintable())
            # update dict/JSON
            ret_dict["choices"][index - 1][info_headers[i]] = temp_string.strip('"')
            i += 1

        index += 1

    return ret_dict


def parser_dict_to_survey(survey_choices, survey_name, user_id, description, minchoices, date_begin, time_begin, date_end, time_end):
    '''
    Parses a dictionary and creates a survey, its choices and their additional infos
    RETURNS created survey's id
    '''

    datetime_begin = date_to_sql_valid(date_begin) + " " +  time_begin
    datetime_end = date_to_sql_valid(date_end) + " " +  time_end

    survey_id = survey_repository.create_new_survey(survey_name, user_id, minchoices, description, datetime_begin, datetime_end)

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

def date_to_sql_valid(date):
    '''
    RETURNS SQL datetime valid date str
    '''
    date = date.split('.')

    return date[2] + "-" + date[1] + "-" + date[0]