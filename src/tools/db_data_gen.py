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
            rejections = ""
            urr.add_user_ranking(user[0], survey_id, ranking, rejections, "")

    def generate_survey(self, user_id):
        name = "PÄIVÄKOTIKYSELY"
        exists = sr.survey_name_exists(name, user_id)
        if exists:
            return
        survey_id = sr.create_new_survey(name, user_id, 10, "AUTOMAATTISESTI GENEROITU!", "2020-01-01 02:03", "2025-01-01 02:02")
        choice_name1 =  "Päiväkoti Aurinkoleikki"
        choice_name2 =  "Päiväkoti Pikku Käpälät"
        choice_name3 =  "Päiväkoti Taikametsä"
        choice_name4 =  "Päiväkoti Satutupa"
        choice_name5 =  "Päiväkoti Onnenkoti"
        choice_name6 =  "Päiväkoti Tähtipolku"
        choice_name7 =  "Päiväkoti Pikkupirtti"
        choice_name8 =  "Päiväkoti Kultakutri"
        choice_name9 =  "Päiväkoti Nallenpesä"
        choice_name10 = "Päiväkoti Ilonpisara"

        #Info generated with ChatGPT :D
        choice_id1 = scr.create_new_survey_choice(survey_id, choice_name1, 11)
        scr.create_new_choice_info(choice_id1, "Opettaja", "Leena Nieminen")
        scr.create_new_choice_info(choice_id1, "Osoite", "Kirkkokatu 8, Tampere")

        choice_id2 = scr.create_new_survey_choice(survey_id, choice_name2, 11)
        scr.create_new_choice_info(choice_id2, "Opettaja", "Juha Virtanen")
        scr.create_new_choice_info(choice_id2, "Osoite", "Peltolantie 12, Vantaa")

        choice_id3 = scr.create_new_survey_choice(survey_id, choice_name3, 11)
        scr.create_new_choice_info(choice_id3, "Opettaja", "Anna Koskinen")
        scr.create_new_choice_info(choice_id3, "Osoite", "Mannerheimintie 15, Helsinki")

        choice_id4 = scr.create_new_survey_choice(survey_id, choice_name4, 11)
        scr.create_new_choice_info(choice_id4, "Opettaja", "Markus Järvinen")
        scr.create_new_choice_info(choice_id4, "Osoite", "Saaristokatu 6, Turku")

        choice_id5 = scr.create_new_survey_choice(survey_id, choice_name5, 11)
        scr.create_new_choice_info(choice_id5, "Opettaja", "Riikka Kallio")
        scr.create_new_choice_info(choice_id5, "Osoite", "Puistokatu 3, Jyväskylä")

        choice_id6 = scr.create_new_survey_choice(survey_id, choice_name6, 11)
        scr.create_new_choice_info(choice_id6, "Opettaja", "Mikko Rantanen")
        scr.create_new_choice_info(choice_id6, "Osoite", "Pohjoinen Rautatiekatu 20, Oulu")

        choice_id7 = scr.create_new_survey_choice(survey_id, choice_name7, 11)
        scr.create_new_choice_info(choice_id7, "Opettaja", "Satu Laine")
        scr.create_new_choice_info(choice_id7, "Osoite", "Kauppakatu 2, Kuopio")

        choice_id8 = scr.create_new_survey_choice(survey_id, choice_name8, 11)
        scr.create_new_choice_info(choice_id8, "Opettaja", "Jari Korhonen")
        scr.create_new_choice_info(choice_id8, "Osoite", "Aleksanterinkatu 14, Lahti")

        choice_id9 = scr.create_new_survey_choice(survey_id, choice_name9, 11)
        scr.create_new_choice_info(choice_id9, "Opettaja", "Maria Virtanen")
        scr.create_new_choice_info(choice_id9, "Osoite", "Rantakatu 5, Joensuu")

        choice_id10 = scr.create_new_survey_choice(survey_id, choice_name10, 11)
        scr.create_new_choice_info(choice_id10, "Opettaja", "Antti Jokinen")
        scr.create_new_choice_info(choice_id10, "Osoite", "Rauhankatu 6, Hämeenlinna")

gen_data = DbDataGen()
