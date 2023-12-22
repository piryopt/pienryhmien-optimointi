import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.user_repository import user_repository as ur
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.services.survey_owners_service import survey_owners_service as sos
from src.entities.user import User
from src.tools.db_tools import clear_database
import json

class TestSurveyChoicesService(unittest.TestCase):
    def setUp(self):
        """
        Creates environment, test users and imports a test survey from json.
        """

        load_dotenv()
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
        self.app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
        db.init_app(self.app)

        self.app_context = self.app.app_context()
        self.app_context.push()

        clear_database()

        user = User("Maija Mallikas", "maija@tester.com", True)
        user2 = User("Tero Testaaja", "tero@tester.com", True)
        ur.register(user)
        ur.register(user2)
        self.user_id = ur.find_by_email(user.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]
        self.user_email = user.email

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        self.survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sos.add_owner_to_survey(self.survey_id, self.user_email)

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_get_list_of_survey_choices_returns_false_if_no_data_found(self):
        '''
        Inputs a nonexistent survey id to getter and checks that return is "False"
        '''
        ret = scs.get_list_of_survey_choices("ITSNOTREAL")
        self.assertEqual(ret, False)

    def test_get_list_of_survey_choices_returns_correct_number_of_choices(self):
        '''
        Tests that get_list_of_survey_choices() returns a list with two members
        '''
        choices = scs.get_list_of_survey_choices(self.survey_id)
        self.assertEqual(len(choices), 2)

    def test_get_list_of_survey_choices_returns_correct_number_of_spaces(self):
        '''
        Tests that get_list_of_survey_choices() returns a list of choices where
        the sum of available spots matches the test data used
        '''
        choices = scs.get_list_of_survey_choices(self.survey_id)
        self.assertEqual(choices[0][3]+choices[1][3], 14)

    def test_get_list_of_survey_choices_returns_correct_choice_names(self):
        '''
        Tests that get_list_of_survey_choices() returns a list of choices where
        the combined choice names matches the input data
        '''
        choices = scs.get_list_of_survey_choices(self.survey_id)
        self.assertEqual(choices[0][2]+" "+choices[1][2],
                         "Esimerkkipäiväkoti 1 Esimerkkipäiväkoti 2")

    def test_get_survey_choice_returns_false_if_survey_not_found(self):
        '''
        Tests that function get_survey_choice() returns false if no
        choice found with the id used as input, uses a string as input
        when ids should be int
        '''
        self.assertEqual(scs.get_survey_choice('Not an id'), False)

    def test_get_survey_choice_gets_correct_choice(self):
        '''
        Fetches all choices with get_list_of_survey_choices() and inputs
        the first result choice id to function get_survey_choice(),
        then tests that the fetched choice names match
        '''
        choices = scs.get_list_of_survey_choices(self.survey_id)
        one_choice = scs.get_survey_choice(choices[0][0])
        self.assertEqual(choices[0][2],one_choice[2])

    def test_get_choice_name_and_spaces_gets_correct_choice(self):
        '''
        Fetches all choices with get_list_of_survey_choices() and inputs
        the first result choice id to function get_choice_name_and_spaces(),
        then tests that the fetched choice names match
        '''
        choices = scs.get_list_of_survey_choices(self.survey_id)
        (id, name, spaces) = scs.get_choice_name_and_spaces(choices[0][0])
        self.assertEqual(choices[0][2],name)

    def test_get_choice_additional_infos_returns_correct_data(self):
        '''
        Fetches all choices with get_list_of_survey_choices() and inputs
        the first result choice id to function get_choice_additional_info(),
        then tests that the fetched additional info is correct
        '''
        choices = scs.get_list_of_survey_choices(self.survey_id)
        choice_infos = scs.get_choice_additional_infos(choices[0][0])
        #headers
        self.assertEqual(choice_infos[0][0]+" "+choice_infos[1][0],
                         "Osoite Postinumero")
        #info
        self.assertEqual(choice_infos[0][1]+" "+choice_infos[1][1],
                         "Keijukaistenpolku 14 00820")

    def test_count_number_of_available_spaces(self):
        '''
        Tests that function count_number_of_available_spaces returns the
        correct number
        '''
        self.assertEqual(scs.count_number_of_available_spaces(self.survey_id),14)

    def test_add_empty_survey_choice(self):
        """
        Tests that function add_empty_survey_choice() adds an empty choice
        with the name "Tyhjä" and the number of seats given when the 
        function was called
        """
        scs.add_empty_survey_choice(self.survey_id, 3)
        choices = scs.get_list_of_survey_choices(self.survey_id)
        self.assertEqual(choices[2][2], "Tyhjä")
        self.assertEqual(choices[2][3], 3)
