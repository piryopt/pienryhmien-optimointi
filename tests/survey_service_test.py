import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.services.survey_service import survey_service as ss
from src.services.survey_choices_service import survey_choices_service as scs
from src.repositories.user_repository import user_repository as ur
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.services.survey_teachers_service import survey_teachers_service as sts
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime
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

        self.setup_users()
        # Remember to add survey choices later (Must be relevant names or tests will fail D:)
        self.edit_dict = {
            "surveyGroupname": "Safest (most dangerous lmao) PED's",
            "surveyInformation": "No way in hell will these have long term affects on your body, mind and soul.",
            "startdate": "01.07.2023",
            "starttime": "00:00",
            "enddate": "31.12.2077",
            "endtime": "00:00",
        }

    def setup_users(self):
        self.ur = ur
        user1 = User("Not on tren Testerr", "feelsbadman@tester.com", True)
        user2 = User("Not on anabolic", "anabolic@tester.com", True)
        user3 = User("trt enjoyer", "ttrt@tester.com", True)
        self.ur.register(user1)
        self.ur.register(user2)
        self.ur.register(user3)
        self.user_id = ur.find_by_email(user1.email)[0]
        self.user_id2 = ur.find_by_email(user2.email)[0]
        self.user_id3 = ur.find_by_email(user3.email)[0]
        self.user_email = user1.email


    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_get_survey_name_nonexisting_id(self):
        """
        Test that no survey name is returned for an invalid survey id
        """
        name = ss.get_survey_name("ITSNOTREAL")
        self.assertEqual(name, False)

    def test_elomake_csv_to_dict_parsing_case_normal(self):
        '''
        Tests that Elomake imported CSV is parsed correctly to a dict
        '''
        file = open("tests/test_files/test_survey1.csv", 'r').read()
        dict = ss.create_survey_from_csv(file)

        choice1 = dict["choices"][0]
        choice2 = dict["choices"][1]

        self.assertEqual(choice1["name"], "Päiväkoti Toivo")
        self.assertEqual(int(choice1["spaces"]), 3)
        self.assertEqual(choice1["Postinumero"], "00790")
        self.assertEqual(choice1["Lisätietoja"], "Tässä tekstiä, pilkulla")

        self.assertEqual(choice2["name"], "Päiväkoti Gehenna")
        self.assertEqual(int(choice2["spaces"]), 6)
        self.assertEqual(choice2["Postinumero"], "00666")
        self.assertEqual(choice2["Lisätietoja"], "Tässä tekstiä,, kahdella pilkulla")

    
    def test_survey_creation_case_normal(self):
        '''
        Tests that dict is parsed correctly to survey, its choices and their additional infos
        CASE NORMAL, the dict is valid etc.
        '''

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], json_object["surveyGroupname"], self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

        # check surveys tables information
        survey_name = ss.get_survey_name(survey_id)
        survey_desc = ss.get_survey_description(survey_id)
        self.assertEqual(survey_name, "Testikysely JSON")
        self.assertEqual(survey_desc, "Tällä testataan kyselyn manuaalista luomista")

        # check choice mandatory informations
        choices = scs.get_list_of_survey_choices(survey_id)
        self.assertEqual(choices[0][2], "Esimerkkipäiväkoti 1")
        self.assertEqual(choices[0][3], 8)
        self.assertEqual(choices[1][2], "Esimerkkipäiväkoti 2")
        self.assertEqual(choices[1][3], 6)

        # check choice additional infos
        choice1_infos = scs.get_choice_additional_infos(choices[0][0])
        choice2_infos = scs.get_choice_additional_infos(choices[1][0])
        self.assertEqual(choice1_infos[0][0], "Osoite")
        self.assertEqual(choice1_infos[0][1], "Keijukaistenpolku 14")
        self.assertEqual(choice1_infos[1][0], "Postinumero")
        self.assertEqual(choice1_infos[1][1], "00820")

        self.assertEqual(choice2_infos[0][0], "Osoite")
        self.assertEqual(choice2_infos[0][1], "Hattulantie 2")
        self.assertEqual(choice2_infos[1][0], "Postinumero")
        self.assertEqual(choice2_infos[1][1], "00550")

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

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 1", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)
        count = ss.count_surveys_created(self.user_id)
        self.assertEqual(count, 1)

    def test_survey_closed(self):
        '''
        Test survey service functions close_survey() and check_if_survey_closed() normal cases
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 2", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

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
        ret = ss.close_survey("ITSNOTREAL", self.user_id)
        self.assertEqual(ret, False)

        ret = ss.check_if_survey_closed("ITSNOTREAL")
        self.assertEqual(ret, False)

    def test_wrong_teacher_cant_close_survey(self):
        '''
        Test that wrong user id can't close an survey
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 3", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

        ret = ss.close_survey(survey_id, self.user_id2)

        self.assertEqual(ret, False)

    def test_get_list_closed_surveys(self):
        '''
        Test only closed surveys are acquired
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        closed_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 4", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(closed_id, self.user_email)
        open_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 5", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(open_id, self.user_email)

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

        closed_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 6", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(closed_id, self.user_email)
        open_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 7", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(open_id, self.user_email)

        ss.close_survey(closed_id, self.user_id)

        surveys = ss.get_active_surveys(self.user_id)

        self.assertEqual(surveys[0][0], open_id)
        self.assertEqual(len(surveys), 1)

    def test_open_survey_normal(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 8", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

        ss.close_survey(survey_id, self.user_id)
        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(closed, True)

        ss.open_survey(survey_id, self.user_id)
        closed = ss.check_if_survey_closed(survey_id)
        self.assertEqual(closed, False)

    def test_open_survey_non_existant(self):
        ret = ss.open_survey("ITSNOTREAL", self.user_id)
        self.assertEqual(ret, False)

    def test_open_survey_wrong_teacher(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 9", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

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
        ret = ss.check_if_survey_results_saved("ITSNOTREAL")
        self.assertEqual(ret, False)
        ret = ss.update_survey_answered("ITSNOTREAL")
        self.assertEqual(ret, False)

        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 10", self.user_id, json_object["surveyInformation"], 1, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

        answered = ss.check_if_survey_results_saved(survey_id)
        self.assertEqual(answered, False)

        ss.update_survey_answered(survey_id)

        answered = ss.check_if_survey_results_saved(survey_id)
        self.assertEqual(answered, True)

    def test_get_survey_as_dict(self):
        '''
        Tests that survey service parser dict correctly
        '''
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 11", self.user_id, json_object["surveyInformation"], 2, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)

        survey_dict = ss.get_survey_as_dict(survey_id)

        # table surveys data
        self.assertEqual(survey_dict["id"], survey_id)
        self.assertEqual(survey_dict["surveyname"], "Test survey 11")
        self.assertEqual(survey_dict["min_choices"], 2)
        self.assertEqual(survey_dict["closed"], False)
        self.assertEqual(survey_dict["results_saved"], False)
        self.assertEqual(survey_dict["survey_description"], json_object["surveyInformation"])
        self.assertEqual(survey_dict["time_begin"], datetime.datetime(2023, 1, 1, 1, 1))
        self.assertEqual(survey_dict["time_end"], datetime.datetime(2024, 1, 1, 2, 2))

        # table survey choices data
        self.assertEqual(survey_dict["choices"][0]["name"], "Esimerkkipäiväkoti 1")
        self.assertEqual(survey_dict["choices"][0]["seats"], 8)
        self.assertEqual(survey_dict["choices"][0]["Osoite"], "Keijukaistenpolku 14")
        self.assertEqual(survey_dict["choices"][0]["Postinumero"], "00820")

        self.assertEqual(survey_dict["choices"][1]["name"], "Esimerkkipäiväkoti 2")
        self.assertEqual(survey_dict["choices"][1]["seats"], 6)
        self.assertEqual(survey_dict["choices"][1]["Osoite"], "Hattulantie 2")
        self.assertEqual(survey_dict["choices"][1]["Postinumero"], "00550")

    def test_get_list_active_answered_invalid(self):
        active_list = ss.get_list_active_answered("ITSNOTREAL")
        self.assertEqual(active_list, [])

    def test_get_list_closed_answered_invalid(self):
        closed_list = ss.get_list_closed_answered("ITSNOTREAL")
        self.assertEqual(closed_list, [])

    def test_get_list_active_answered(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 12", self.user_id, json_object["surveyInformation"], 2, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)
        ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id3, survey_id, ranking, "", "")
        active_list = ss.get_list_active_answered(self.user_id3)
        self.assertEqual(1, len(active_list))

    def test_get_list_closed_answered(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 12", self.user_id, json_object["surveyInformation"], 2, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)
        ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id3, survey_id, ranking, "", "")
        ss.close_survey(survey_id, self.user_id)
        closed_list = ss.get_list_closed_answered(self.user_id3)
        self.assertEqual(1, len(closed_list))

    def test_check_surveys_to_close_empty(self):
        """
        Test that the function works when no open surveys
        """
        clear_database()
        self.setup_users()
        surveys = ss.check_for_surveys_to_close()
        self.assertEqual(False, surveys)

    def test_check_surveys_to_close(self):
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)

        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 13", self.user_id, json_object["surveyInformation"], 2, "01.01.2023", "01:01", "01.01.2024", "02:02")
        sts.add_teacher_to_survey(survey_id, self.user_email)
        survey_id2 = ss.create_new_survey_manual(json_object["choices"], "Test survey 14", self.user_id, json_object["surveyInformation"], 2, "01.01.1998", "01:01", "01.01.1999", "02:02")
        sts.add_teacher_to_survey(survey_id2, self.user_email)
        surveys = ss.check_for_surveys_to_close()
        closed = ss.check_if_survey_closed(survey_id2)
        self.assertEqual(True, closed)

    def test_save_survey_edit(self):
        """
        Test that editing a survey works
        """
        with open("tests/test_files/test_survey1.json", 'r') as openfile:
            # open as JSON instead of TextIOWrapper or something
            json_object = json.load(openfile)
        survey_id = ss.create_new_survey_manual(json_object["choices"], "Test survey 15", self.user_id, json_object["surveyInformation"], 2, "01.01.2023", "01:01", "01.01.2024", "02:02")
        ss.save_survey_edit(survey_id, self.edit_dict, self.user_id)
        name = ss.get_survey_name(survey_id)
        self.assertEqual(name, "Safest (most dangerous lmao) PED's")
        desc = ss.get_survey_description(survey_id)
        self.assertEqual(desc, "No way in hell will these have long term affects on your body, mind and soul.")
