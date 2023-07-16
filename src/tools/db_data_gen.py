from random import choice, shuffle
from src.entities.user import User
from src.repositories.user_repository import user_repository as ur
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.survey_choices_repository import survey_choices_repository as scr
from src.repositories.user_rankings_repository import user_rankings_repository as urr


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
            name = firstname + " " + lastname
            student_number = "01"
            for i in range(7):
                student_number += str(choice(self.numbers))
            email = firstname.lower() + "." + lastname.lower() + "@test.com"
            new_user = User(name, student_number, email, False)
            self.users.append(new_user)

    def add_generated_users_db(self):
        for user in self.users:
            ur.register(user)

    def generate_rankings(self, survey_id):
        survey_choices = scr.find_survey_choices(survey_id)
        choice_ids = []
        for choice in survey_choices:
            choice_ids.append(str(choice[0]))

        db_users = ur.get_all_users()
        for user in db_users:
            shuffle(choice_ids)
            ranking = ','.join(choice_ids)
            urr.add_user_ranking(user[0], survey_id, ranking)

    def generate_survey(self, user_id):
        name = "GENERATED SURVEY"
        exists = sr.survey_name_exists(name, user_id)
        if exists:
            return
        survey_id = sr.add_new_survey(name, user_id)
        choice_name1 = "Weather-based recommendation for outdoor activities in Helsinki"
        choice_name2 = "Sovellus pienryhmien optimointiin eli miten jakaa opiskelijat pienryhmiin heidän kiinnostusten perusteella?"
        choice_name3 = "Seamless TinyML lifecycle management"
        choice_name4 = "Improved tools for data scientists"
        choice_name5 = "Automatic local news generator with Generative AI"
        choice_name6 = "Berry Picker Tracker"
        choice_name7 = "Urheiluseura 3.0"
        choice_name8 = "BookCine: the movie-book recommender system"
        choice_name9 = "Ohjelmistotuotantoprojektien ilmoittautumissovelluksen laajennus"
        choice_name10 = "Tietojen importti/exporttityökalu MammalBaseen"

        #Info generated with ChatGPT :D
        scr.add_new_survey_choice(survey_id, choice_name1, 11,  "Leena Nieminen", "Kirkkokatu 8, Tampere")
        scr.add_new_survey_choice(survey_id, choice_name2, 11, "Juha Virtanen", "Peltolantie 12, Vantaa")
        scr.add_new_survey_choice(survey_id, choice_name3, 11, "Anna Koskinen", "Mannerheimintie 15, Helsinki")
        scr.add_new_survey_choice(survey_id, choice_name4, 11, "Markus Järvinen", "Saaristokatu 6, Turku")
        scr.add_new_survey_choice(survey_id, choice_name5, 11, "Riikka Kallio", "Puistokatu 3, Jyväskylä")
        scr.add_new_survey_choice(survey_id, choice_name6, 11, "Mikko Rantanen", "Pohjoinen Rautatiekatu 20, Oulu")
        scr.add_new_survey_choice(survey_id, choice_name7, 11, "Satu Laine", "Kauppakatu 2, Kuopio")
        scr.add_new_survey_choice(survey_id, choice_name8, 11, "Jari Korhonen", "Aleksanterinkatu 14, Lahti")
        scr.add_new_survey_choice(survey_id, choice_name9, 11, "Maria Virtanen", "Rantakatu 5, Joensuu")
        scr.add_new_survey_choice(survey_id, choice_name10, 11, "Antti Jokinen", "Rauhankatu 6, Hämeenlinna")

gen_data = DbDataGen()
