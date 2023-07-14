def convert_to_list(ranking_string):
    ranking_list = ranking_string.split(",")
    return ranking_list

def convert_to_string(ranking_list):
    ranking_string = ','.join(ranking_list)
    return ranking_string
