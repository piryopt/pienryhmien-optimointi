from src.repositories.survey_repository import survey_repository
from src.repositories.survey_choices_repository import survey_choices_repository

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
    print(first_row)
    print(col_count)

    # add column headers to own array
    for cell in first_row:
        # remove unseen control characters etc.
        temp = ''.join(c for c in cell if c.isprintable())
        # remove leftover " from parsing
        info_headers.append(temp.strip('"'))

    index = 0
    for line in file:
        print(line)
        # bad, but using file[index] doesn't work
        if index == row_count - 1:
            break
        if index == 0:
            index += 1
            continue

        temp = line.split('''","''')
        name = ''.join(c for c in temp[2] if c.isprintable())
        spaces = ''.join(c for c in temp[3] if c.isprintable()).strip('"')
        min_size = ''.join(c for c in temp[4] if c.isprintable()).strip('"')

        # update dict/JSON
        ret_dict["choices"].append({})
        ret_dict["choices"][index - 1]["name"] = name
        ret_dict["choices"][index - 1]["spaces"] = spaces
        ret_dict["choices"][index - 1]["min_size"] = min_size

        i = 5
        while i < col_count:
            temp_string = ''.join(c for c in temp[i] if c.isprintable())
            # update dict/JSON
            ret_dict["choices"][index - 1][info_headers[i]] = temp_string.strip('"')
            i += 1

        index += 1

    return ret_dict


def parser_dict_to_survey(survey_choices, survey_name, description, minchoices, date_begin, time_begin, date_end, time_end, allowed_denied_choices, allow_search_visibility):
    '''
    Parses a dictionary and creates a survey, its choices and their additional infos
    RETURNS created survey's id
    '''

    datetime_begin = date_to_sql_valid(date_begin) + " " +  time_begin
    datetime_end = date_to_sql_valid(date_end) + " " +  time_end

    survey_id = survey_repository.create_new_survey(survey_name, minchoices, description, datetime_begin, datetime_end, allowed_denied_choices, allow_search_visibility)

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
    survey_dict["time_begin"] = survey[6]
    survey_dict["time_end"] = survey[7]
    survey_dict["allow_search_visibility"] = survey[9]

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
