def convert_to_list(ranking_string):
    """
    Converts a string consisting of the rankings of a survey into a list. E.G "2,3,5,6,4,7" -> ["2", "3", "5", "6", "4", "7"]

    args:
        ranking_string: The string that is converted into a list. The string is retrieved from the database table user_survey_rankings
    """
    if ranking_string == "":
        return []
    ranking_list = ranking_string.split(",")
    return ranking_list

def convert_to_int_list(ranking_string):
    """
    Converts a list consisting of the rankings of a survey into a list of integers. E.G ["2", "3", "5", "6", "4", "7"] -> [2, 3, 5, 6, 4, 7]

    args:
        ranking_list: The list that is converted into a list of integers. The list is retrieved from the database table user_survey_rankings
    """
    if ranking_string == '':
        return []
    ranking_list = ranking_string.split(",")

    int_ranking = [int(i) for i in ranking_list]

    return int_ranking

def convert_to_string(ranking_list):
    """
    Converts a list consisting of the rankings of a survey into a string. E:G ["2", "3", "5", "6", "4", "7"] -> "2,3,5,6,4,7"

    args:
        ranking_list: The list of rankings that the user chooses. It is converted into a string which is need when adding rankings
        to the database
    """
    ranking_string = ",".join(ranking_list)
    return ranking_string
