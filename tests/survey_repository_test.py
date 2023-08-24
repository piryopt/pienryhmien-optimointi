import unittest
import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.repositories.survey_repository import survey_repository as sr
from src.repositories.user_repository import user_repository as ur
from src.repositories.user_rankings_repository import user_rankings_repository as urr
from src.repositories.survey_teachers_repository import survey_teachers_repository as st
from src.entities.user import User
from src.tools.db_tools import clear_database
import datetime

class TestSurveyRepository(unittest.TestCase):
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

    def tearDown(self):
        db.drop_all()
        self.app_context.pop()

    def test_get_survey(self):
        """
        Create new survey and test if it exists and also test if the surveyname exists
        """
        survey_id = sr.create_new_survey("Test survey 1", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        survey = sr.get_survey(survey_id)
        self.assertEqual(survey[0], survey_id)

    def test_check_that_survey_doesnt_exist(self):
        """
        Test that survey with invalid id doesn't exist
        """
        exists = sr.get_survey("ITSNOTREAL")
        self.assertEqual(False, exists)

    def test_survey_name_doesnt_exist(self):
        """
        Test that surveyname doesn't exist
        """
        survey_name = "Test survey 2"
        exists = sr.survey_name_exists(survey_name, self.user_id)
        self.assertEqual(False, exists)

    def test_count_created_surveys(self):
        """
        Test that the number of created surveys is correct
        """

        survey_id1 = sr.create_new_survey("Test survey 3", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        survey_id2 = sr.create_new_survey("Test survey 4", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id1, self.user_id2)
        st.add_teacher_to_survey(survey_id2, self.user_id2)
        count = sr.count_created_surveys(self.user_id2)
        self.assertEqual(2, count)

    def test_close_survey(self):
        """
        Test that closing a survey works
        """
        survey_id = sr.create_new_survey("Test survey 5", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id2)
        sr.close_survey(survey_id)

        closed = sr.get_survey(survey_id).closed
        self.assertEqual(True, closed)

    def test_get_active_surveys(self):
        """
        Test that getting a list of active surveys works
        """
        survey_id = sr.create_new_survey("Test survey 6", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id2)
        active_list = sr.get_active_surveys(self.user_id2)
        self.assertEqual(1, len(active_list))

    def test_get_closed_surveys(self):
        """
        Test that getting a list of closed surveys works
        """
        survey_id = sr.create_new_survey("Test survey 7", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id2)
        sr.close_survey(survey_id)
        closed_list = sr.get_closed_surveys(self.user_id2)
        self.assertEqual(1, len(closed_list))

    def test_open_survey(self):
        """
        Test that closing a survey works
        """
        survey_id = sr.create_new_survey("Test survey 8", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        sr.close_survey(survey_id)

        closed = sr.get_survey(survey_id).closed
        self.assertEqual(True, closed)

        sr.open_survey(survey_id)
        opened = sr.get_survey(survey_id).closed
        self.assertEqual(False, opened)

    def test_survey_name_exists(self):
        """
        Test that a survey name exists when a survey is added to the database
        """
        survey_id = sr.create_new_survey("Test survey 9", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        exists = sr.survey_name_exists("Test survey 9", self.user_id)
        self.assertEqual(True, exists)

    def test_count_created_surveys_invalid_id(self):
        """
        Test that the function behaves correctly when trying to get the list of all created surveys for an invalid user
        """
        exists = sr.count_created_surveys(-1)
        self.assertEqual(False, exists)

    def test_count_active_surveys_invalid_id(self):
        """
        Test that the function behaves correctly when trying to get the list of active created surveys for an invalid user
        """
        exists = sr.get_active_surveys(-1)
        self.assertEqual(False, exists)

    def test_survey_description(self):
        """
        Test that getting the description of a survey works
        """
        survey_id = sr.create_new_survey("Test survey 10", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        desc = sr.get_survey_description(survey_id)
        self.assertEqual("Motivaatio", desc)

    def test_survey_answered(self):
        """
        Test that updating a survey so that it has its results saved works
        """
        survey_id = sr.create_new_survey("Test survey 11", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        sr.update_survey_answered(survey_id)
        answered = sr.get_survey(survey_id).results_saved
        self.assertEqual(True, answered)

    def test_survey_time_begin_correct(self):
        """
        Test that the begin time of a created survey is correct
        """
        survey_id = sr.create_new_survey("Test survey 12", 10, "Ei motivaatiota", "2023-01-01 02:03", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        time = sr.get_survey_time_begin(survey_id)

        self.assertEqual(time, datetime.datetime(2023, 1, 1, 2, 3))

    def test_survey_time_end_correct(self):
        """
        Test that the ending time of a created survey is correct
        """
        survey_id = sr.create_new_survey("Test survey 13", 10, "Ei motivaatiota", "2023-10-02 13:01", "2024-06-19 12:01")
        st.add_teacher_to_survey(survey_id, self.user_id)
        time = sr.get_survey_time_end(survey_id)

        self.assertEqual(time, datetime.datetime(2024, 6, 19, 12, 1))

    def test_get_list_active_answered(self):
        """
        Test that the list of active surveys which the student has answered is the correct length
        """
        survey_id = sr.create_new_survey("Test survey 14", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id3, survey_id, ranking, "", "")
        active_answered = sr.get_list_active_answered(self.user_id3)
        self.assertEqual(1, len(active_answered))

    def test_get_list_closed_answered(self):
        """
        Test that the list of closed surveys which the student has answered is the correct length
        """
        survey_id = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        ranking = "2,3,5,4,1,6"
        urr.add_user_ranking(self.user_id3, survey_id, ranking, "", "")
        sr.close_survey(survey_id)
        closed_answered = sr.get_list_closed_answered(self.user_id3)
        self.assertEqual(1, len(closed_answered))

    def test_get_list_active_answered_invalid(self):
        """
        Test that getting the list of active surveys of an invalid account works
        """
        active_answered = sr.get_list_active_answered(-1)
        self.assertEqual(active_answered, False)

    def test_get_list_closed_answered_invalid(self):
        """
        Test that getting the list of closed surveys of an invalid account works
        """
        closed_answered = sr.get_list_closed_answered(-1)
        self.assertEqual(closed_answered, False)

    def test_get_list_all_open_surveys(self):
        """
        Test that the amount of all open surveys is correct. The database is emptied before the test
        """
        clear_database()
        self.setup_users()
        survey_id1 = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id1, self.user_id)
        survey_id2 = sr.create_new_survey("Test survey 16", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id2, self.user_id2)
        survey_id3 = sr.create_new_survey("Test survey 17", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id3, self.user_id)
        sr.close_survey(survey_id3)
        all_open_surveys =sr.get_all_active_surveys()
        self.assertEqual(2, len(all_open_surveys))

    def test_save_survey_edit(self):
        """
        Test that editing a survey works
        """
        survey_id = sr.create_new_survey("Test survey 15", 10, "Motivaatio", "2023-01-01 01:01", "2024-01-01 02:02")
        st.add_teacher_to_survey(survey_id, self.user_id)
        sr.save_survey_edit(survey_id, "Edited survey", "moti", "2023-01-01 01:01", "2024-01-01 02:02")
        survey = sr.get_survey(survey_id)
        self.assertEqual(survey.surveyname, "Edited survey")
        self.assertEqual(survey.survey_description, "moti")
