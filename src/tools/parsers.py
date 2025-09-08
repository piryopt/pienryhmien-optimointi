import csv
from io import StringIO
import pandas as pd
from src.repositories.survey_repository import survey_repository
from src.repositories.survey_choices_repository import survey_choices_repository

def parser_csv_to_dict(file):
    '''
    Parses an imported CSV to a dictionary,
    the dictionary is later used by parser_manual() (below)
    RETURNS dictionary that can be parsed by later functions
    '''

    f = StringIO(file)

    try:
        dialect = csv.Sniffer().sniff(file[:1024])
        delimiter = dialect.delimiter
    except Exception:
        delimiter = ';'

    reader = pd.read_csv(f, sep=delimiter, dtype=str)

    ret_dict = {"choices": []}
    columns = list(reader.columns)
    col_count = len(columns)

    for row in reader.values:
        choice = {
            "name": row[0],
            "spaces": row[1],
            "min_size": row[2]
        }

        for i in range(3, col_count):
            choice[columns[i]] = row[i]

        ret_dict["choices"].append(choice)

    return ret_dict


def parser_dict_to_survey(survey_choices, survey_name, description, minchoices, date_end, time_end, allowed_denied_choices, allow_search_visibility):
    '''
    Parses a dictionary and creates a survey, its choices and their additional infos
    RETURNS created survey's id
    '''

    datetime_end = date_to_sql_valid(date_end) + " " +  time_end

    survey_id = survey_repository.create_new_survey(survey_name, minchoices, description, datetime_end, allowed_denied_choices, allow_search_visibility)

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
                continue
            if count == 2:
                min_size = choice[pair]
                count += 1
                choice_id = survey_choices_repository.create_new_survey_choice(survey_id, name, spaces, min_size)
                continue

            hidden = False

            if pair[-1] == '*':
                hidden = True

            survey_choices_repository.create_new_choice_info(choice_id, pair, choice[pair], hidden)
            count += 1

    return survey_id

def parser_existing_survey_to_dict(survey_id):
    '''
    Parses existing survey, its choices and their infos into a dict
    RETURNS dictionary of survey data
    '''
    survey_dict = {}

    survey = survey_repository.get_survey(survey_id)

    survey_dict["id"] = survey[0]
    survey_dict["surveyname"] = survey[1]
    survey_dict["min_choices"] = survey[2]
    survey_dict["closed"] = survey[3]
    survey_dict["results_saved"] = survey[4]
    survey_dict["survey_description"] = survey[5]
    survey_dict["time_end"] = survey[6]
    survey_dict["allow_search_visibility"] = survey[8]

    survey_choices = survey_choices_repository.find_survey_choices(survey_id)
    survey_dict["choices"] = []

    index = 0
    for row in survey_choices:
        survey_dict["choices"].append({})
        survey_dict["choices"][index]["id"] = row[0]
        survey_dict["choices"][index]["name"] = row[2]
        survey_dict["choices"][index]["seats"] = row[3]
        survey_dict["choices"][index]["min_size"] = row[5]

        additional_infos = survey_choices_repository.get_choice_additional_infos(row[0])

        for info in additional_infos:
            print(info)
            survey_dict["choices"][index][info[0]] = info[1]

        index += 1

    return survey_dict

def date_to_sql_valid(date):
    '''
    RETURNS SQL datetime valid date str
    '''
    date = date.split('.')

    return date[2] + "-" + date[1] + "-" + date[0]
