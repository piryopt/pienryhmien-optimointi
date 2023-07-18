import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.entities.user import User
from src.tools.db_tools import clear_database
import json

class TestSurveyService(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        clear_database()

        user = User("Not on tren Testerr", 101010101, "tren4lyfe@tester.com", True)
        user2 = User("Hashtag natty", 101010101, "anabolics4lyfe@tester.com", True)
        ur.register(user)
        ur.register(user2)
        self.user_id = ur.find_by_email(user.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]


    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_get_survey_name_nonexisting_id(self):
        """
        Test that no survey name is returned for an invalid survey id
        """
        name = ss.get_survey_name(-1)
        self.assertEqual(name, False)

    
    def test_manual_survey_creation_case_normal(self):

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        # check surveys tables information
        survey_name = ss.get_survey_name(survey_id)
        survey_desc = ss.get_survey_description(survey_id)
        self.assertEqual(survey_name, "Testikysely JSON")
        self.assertEqual(survey_desc, "Tällä testataan manuaalista luomista")

        # check choice mandatory informations
        choices = scs.get_list_of_survey_choices(survey_id)
        self.assertEqual(choices[0][2], "Ensimmäinen choice")
        self.assertEqual(choices[0][3], 8)
        self.assertEqual(choices[1][2], "Toinen choice")
        self.assertEqual(choices[1][3], 6)

        # check choice additional infos
        choice1_infos = scs.get_choice_additional_infos(choices[0][0])
        choice2_infos = scs.get_choice_additional_infos(choices[1][0])
        self.assertEqual(choice1_infos[0][0], "Eka lisätieto")
        self.assertEqual(choice1_infos[0][1], "vaikeuksia csv testaamisessa")
        self.assertEqual(choice1_infos[1][0], "Postinumero")
        self.assertEqual(choice1_infos[1][1], "00790")

        self.assertEqual(choice2_infos[0][0], "Eka lisätieto")
        self.assertEqual(choice2_infos[0][1], "äisimhi tunappat nelo")
        self.assertEqual(choice2_infos[1][0], "Postinumero")
        self.assertEqual(choice2_infos[1][1], "01820")

    def test_csv_survey_creation_case_normal(self):

        file = open("tests/test_files/test_survey1.csv")
        # Convert textwrapper or something so string
        file = file.read()
        survey_id = ss.create_survey_from_csv(file, "CSV testikysely", self.user_id, "CSV kuvaus")

        # check surveys tables information
        survey_name = ss.get_survey_name(survey_id)
        survey_desc = ss.get_survey_description(survey_id)
        self.assertEqual(survey_name, "CSV testikysely")
        self.assertEqual(survey_desc, "CSV kuvaus")

        # check choice mandatory informations
        choices = scs.get_list_of_survey_choices(survey_id)
        self.assertEqual(choices[0][2], "Päiväkoti Toivo")
        self.assertEqual(choices[0][3], 3)
        self.assertEqual(choices[1][2], "Päiväkoti Gehenna")
        self.assertEqual(choices[1][3], 6)

        # check choice additional infos
        choice1_infos = scs.get_choice_additional_infos(choices[0][0])
        choice2_infos = scs.get_choice_additional_infos(choices[1][0])
        self.assertEqual(choice1_infos[0][0], "Postinumero")
        self.assertEqual(choice1_infos[0][1], "00790")
        self.assertEqual(choice1_infos[1][0], "Lisätietoja")
        self.assertEqual(choice1_infos[1][1], "Tässä tekstiä, pilkulla")

        self.assertEqual(choice2_infos[0][0], "Postinumero")
        self.assertEqual(choice2_infos[0][1], "00666")
        self.assertEqual(choice2_infos[1][0], "Lisätietoja")
        self.assertEqual(choice2_infos[1][1], "Tässä tekstiä,, kahdella pilkulla")
