from random import choice, shuffle
from src.entities.user import User
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_repository import survey_repository as sr


class DbDataGen:
    def __init__(self):
        self.firstnames = ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph",
                           "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
                             "Donald", "Steven", "Andrew", "Paul", "Joshua", "Mary", "Patricia", "Jennifer",
                               "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen", "Lisa",
                                 "Nancy", "Betty", "Sandra", "Margaret", "Ashley", "Kimberly", "Emily", "Donna", "Michelle"]
        
        self.lastnames = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez",
                           "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore",
                             "Martin", "Jackson", "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis",
                               "Robinson", "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
                               ,"Green" ,"Adams" ,"Nelson" ,"Baker" ,"Hall" ,"Rivera" ,"Campbell" ,"Mitchell" ,"Carter" ,"Roberts"]
        
        self.numbers = [0,1,2,3,4,5,6,7,8,9]
        self.users = []
        
    def generate_users(self, n):
        for i in range(n):
            firstname = choice(self.firstnames)
            lastname = choice(self.lastnames)
            student_number = "01"
            for i in range(7):
                student_number += str(choice(self.numbers))
            email = firstname.lower() + "." + lastname.lower() + "@test.com"
            new_user = User(firstname, lastname, student_number, email, "motivaatio", False)
            self.users.append(new_user)

    def add_generated_users_db(self):
        for user in self.users:
            ur.register(user)

    def generate_rankings(self, survey_id):
        survey_choices = sr.find_survey_choices(survey_id)
        choice_ids = []
        for choice in survey_choices:
            choice_ids.append(str(choice[0]))

        db_users = ur.get_all_users()
        for user in db_users:
            shuffle(choice_ids)
            ranking = ','.join(choice_ids)
            sr.add_user_ranking(user[0], survey_id, ranking)

gen_data = DbDataGen()
