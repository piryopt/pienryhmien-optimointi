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

    def test_count_surveys_created(self):
        '''
        Test survey service function count_surveys_created()
        UPDATE WHEN SURVEYS OF SAME NAME NO LONGER ACCEPTED
        '''
        count = ss.count_surveys_created(self.user_id)
        self.assertEqual(count, 0)

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        count = ss.count_surveys_created(self.user_id)
        self.assertEqual(count, 1)

    def test_survey_closed(self):
        '''
        Test survey service functions close_survey() and check_if_survey_closed() normal cases
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(closed, False)

        ss.close_survey(survey_id, self.user_id)
        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(closed, True)

    def test_close_non_existing_survey(self):
        '''
        Test survey service functions close_survey() and check_if_survey_closed() non existing cases
        doesn't differentiate between non-existing and closed, might be a problem
        '''
        ret = ss.close_survey(-1, self.user_id)
        self.assertEqual(ret, False)

        ret = ss.check_if_survey_closed(-1)
        self.assertEqual(ret, False)

    def test_wrong_teacher_cant_close_survey(self):
        '''
        Test that wrong user id can't close an survey
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        ret = ss.close_survey(survey_id, self.user_id2)

        self.assertEqual(ret, False)

    def test_get_list_closed_surveys(self):
        '''
        Test only closed surveys are acquired
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        closed_id = ss.create_new_survey_manual(json_object["choices"], "Suljettu", self.user_id, json_object["surveyInformation"])
        open_id = ss.create_new_survey_manual(json_object["choices"], "Avoin", self.user_id, json_object["surveyInformation"])

        ss.close_survey(closed_id, self.user_id)

        surveys = ss.get_list_closed_surveys(self.user_id)

        self.assertEqual(surveys[0][0], closed_id)
        self.assertEqual(len(surveys), 1)

    def test_get_list_open_surveys(self):
        '''
        Test only open surveys are acquired
        '''

        # first check 0 surveys branch
        surveys = ss.get_active_surveys(self.user_id)
        self.assertEqual(surveys, False)

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        closed_id = ss.create_new_survey_manual(json_object["choices"], "Suljettu", self.user_id, json_object["surveyInformation"])
        open_id = ss.create_new_survey_manual(json_object["choices"], "Avoin", self.user_id, json_object["surveyInformation"])

        ss.close_survey(closed_id, self.user_id)

        surveys = ss.get_active_surveys(self.user_id)

        self.assertEqual(surveys[0][0], open_id)
        self.assertEqual(len(surveys), 1)

    def test_open_survey_normal(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        ss.close_survey(survey_id, self.user_id)
        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(closed, True)

        ss.open_survey(survey_id, self.user_id)
        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(closed, False)

    def test_open_survey_non_existant(self):

        ret = ss.open_survey(-1, self.user_id)
        self.assertEqual(ret, False)

    def test_open_survey_wrong_teacher(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        ss.close_survey(survey_id, self.user_id)
        ret = ss.open_survey(survey_id, self.user_id2)
        self.assertEqual(ret, False)

        ret = ss.check_if_survey_closed(survey_id)
        self.assertEqual(ret, True)

    def test_check_if_survey_results_saved(self):
        '''
        Test functions update_survey_answered() and check_if_survey_results_saved()
        '''

        # first check non existant case
        ret = ss.check_if_survey_results_saved(-1)
        self.assertEqual(ret, False)
        ret = ss.update_survey_answered(-1)
        self.assertEqual(ret, False)

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"])

        answered = ss.check_if_survey_results_saved(survey_id)
        self.assertEqual(answered, False)

        ss.update_survey_answered(survey_id)

        answered = ss.check_if_survey_results_saved(survey_id)
        self.assertEqual(answered, True)
