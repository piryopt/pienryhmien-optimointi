import pandas
from src.entities.user import User
from src.repositories.user_repository import user_repository as ur
from src.repositories.user_rankings_repository import user_rankings_repository as urr

survey_id = 'VZ3Ai8XEcz'

survey_choices = {}
survey_choices['Group 1'] = '3843'
survey_choices['Group 2'] = '3844'
survey_choices['Group 3'] = '3845'
survey_choices['Group 4'] = '3846'
survey_choices['Group 5'] = '3847'
survey_choices['Group 6'] = '3848'
survey_choices['Group 7'] = '3849'
survey_choices['Group 8'] = '3850'
survey_choices['Group 9'] = '3851'
survey_choices['Group 10'] = '3852'
survey_choices['Group 11'] = '3853'
survey_choices['Group 12'] = '3854'
survey_choices['Group 13'] = '3855'
survey_choices['Group 14'] = '3856'
survey_choices['Group 15'] = '3857'
survey_choices['Group 16'] = '3858'

csvfile = pandas.read_csv('students_data.csv')

def read_file():
    for row in csvfile.values:
        name = row[1] + ' ' + row[0]
        email = row[3]

        new_user = User(name, email, False)
        ur.register(new_user)
        
        choices = []
        for i in range(4, len(row)):
            choices.append(survey_choices[row[i]])
        ranking = ','.join(choices)

        user_id = ur.get_user_by_email(email)[0]
        urr.add_user_ranking(user_id, survey_id, ranking, '', '')





