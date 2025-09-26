from sqlalchemy import text
from src import db
from src.tools.db_tools import generate_unique_id


class SurveyRepository:
    def get_survey(self, survey_id):
        """
        SQL code for getting all data from a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT * FROM surveys WHERE id=:survey_id"
            result = db.session.execute(text(sql), {"survey_id": survey_id})
            survey = result.fetchone()
            if not survey:
                return False
            return survey
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def survey_name_exists(self, surveyname, user_id):
        """
        SQL code for getting the id from a survey that has a certain name, is open has access to by a certain user.

        args:
            surveyname: The name of the survey
            user_id: The id of the user
        """
        try:
            sql = "SELECT s.id FROM surveys s, survey_owners so WHERE (s.surveyname=:surveyname AND so.user_id=:user_id AND s.closed=False AND so.survey_id=s.id AND s.deleted=False)"
            result = db.session.execute(text(sql), {"surveyname": surveyname, "user_id": user_id})
            survey = result.fetchone()
            if not survey:
                return False
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def count_created_surveys(self, user_id):
        """
        SQL code for getting the number of surveys the owner has access to

        args:
            user_id: The id of the user
        """
        # Do we want to diplay all surveys created or only the active ones?
        try:
            sql = "SELECT s.id FROM surveys s, survey_owners so WHERE (so.user_id=:user_id AND so.survey_id=s.id)"
            result = db.session.execute(text(sql), {"user_id": user_id})
            survey_list = result.fetchall()
            if not survey_list:
                return False
            return len(survey_list)
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def close_survey(self, survey_id):
        """
        SQL code for closing a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET closed = True WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def open_survey(self, survey_id):
        """
        SQL code for opening a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET closed = False WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_active_surveys(self, user_id):
        """
        SQL code getting the list of all active surveys for which the user has access to.

        args:
            user_id: The id of the user
        """
        try:
            sql = "SELECT s.id, s.surveyname FROM surveys s, survey_owners so WHERE (so.user_id=:user_id AND closed=False AND s.id=so.survey_id AND s.deleted=False)"
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_closed_surveys(self, user_id):
        """
        SQL code getting the list of all closed surveys for which the owner has access to.

        args:
            user_id: The id of the user
        """
        try:
            sql = "SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end FROM surveys s, survey_owners so WHERE (so.user_id=:user_id AND s.closed=True AND so.survey_id = s.id AND s.deleted=False) ORDER BY s.time_end DESC"
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def update_survey_answered(self, survey_id):
        """
        SQL code for updating result_saved of the surveys table from False to True

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET results_saved = True WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def create_new_survey(self, surveyname, min_choices, description, enddate, allowed_denied_choices=0, allow_search_visibility=True):
        """
        Creates a new survey, updates just surveys table
        RETURNS created survey's id
        """
        try:
            id = generate_unique_id(10)
            while self.get_survey(id):
                id = generate_unique_id(10)

            sql = (
                "INSERT INTO surveys (id, surveyname, min_choices, closed, results_saved, survey_description, time_end, allowed_denied_choices, allow_search_visibility, deleted)"
                " VALUES (:id, :surveyname, :min_choices, :closed, :saved, :desc, :t_e, :a_d_c, :a_s_v, False) RETURNING id"
            )

            result = db.session.execute(
                text(sql),
                {
                    "id": id,
                    "surveyname": surveyname,
                    "min_choices": min_choices,
                    "closed": False,
                    "saved": False,
                    "desc": description,
                    "t_e": enddate,
                    "a_d_c": allowed_denied_choices,
                    "a_s_v": allow_search_visibility,
                },
            )
            db.session.commit()
            return result.fetchone()[0]
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_survey_description(self, survey_id):
        """
        SQL code for getting the desctiption of a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT survey_description FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id": survey_id})
            return result.fetchone()[0]
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_survey_time_end(self, survey_id):
        """
        RETURNS date and time as datetime.datetime(year, month, day, hour, minute)
        """
        try:
            sql = "SELECT time_end FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id": survey_id})
            return result.fetchone()[0]
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_survey_min_choices(self, survey_id):
        """
        Returns the amount of minumum answers required in the survey.

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT min_choices FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id": survey_id})
            return result.fetchone()[0]
        except Exception as e:
            print(e)
            return False

    def get_survey_max_denied_choices(self, survey_id):
        """
        Returns the maximum amount of denied choices the survey allows.

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT allowed_denied_choices FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id": survey_id})
            return result.fetchone()[0]
        except Exception as e:
            print(e)
            return False

    def get_survey_search_visibility(self, survey_id):
        """
        Returns the search visibility preference of the survey.

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT allow_search_visibility FROM surveys WHERE id=:id"
            result = db.session.execute(text(sql), {"id": survey_id})
            return result.fetchone()[0]
        except Exception as e:
            print(e)
            return False

    def fetch_all_active_surveys(self, user_id):
        """Returns a list of all surveys in the database"""
        sql = text(
            "SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end FROM surveys s, survey_owners so WHERE (so.user_id=:user_id AND s.closed=False AND s.id=so.survey_id AND s.deleted=False)"
        )
        result = db.session.execute(sql, {"user_id": user_id})
        all_surveys = result.fetchall()
        return all_surveys

    def fetch_survey_responses(self, survey_id):
        """Returns a list of answers submitted to a certain survey"""
        try:
            sql = text("SELECT user_id, ranking, rejections, reason FROM user_survey_rankings " + "WHERE survey_id=:survey_id AND deleted IS FALSE")
            result = db.session.execute(sql, {"survey_id": survey_id})
            responses = result.fetchall()
            if not responses:
                return False
            return responses
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_list_active_answered(self, user_id):
        """
        SQL code for getting a list of surveys that are active, that have been answered by the user

        args:
            user_id: The id of the user
        """
        try:
            sql = (
                "SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end FROM surveys s, user_survey_rankings r"
                "  WHERE (r.survey_id=s.id AND r.user_id=:user_id AND s.closed = False AND r.deleted = False AND s.deleted=False)"
            )
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_list_closed_answered(self, user_id):
        """
        SQL code for getting a list of surveys that are closed, that have been answered by the user

        args:
            user_id: The id of the user
        """
        try:
            sql = (
                "SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end FROM surveys s, user_survey_rankings r"
                "  WHERE (r.survey_id=s.id AND r.user_id=:user_id AND s.closed = True AND r.deleted = False AND s.deleted=False)"
            )
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_all_active_surveys(self):
        """
        SQL code for getting all active surveys. Needed for automatic closing which will be checked every hour.
        """
        try:
            sql = "SELECT * FROM surveys WHERE (closed=False AND deleted=False)"
            result = db.session.execute(text(sql))
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_all_active_survey_admin_data(self):
        """
        Get all relevant survey data for the admin page
        """
        try:
            sql = "SELECT id, surveyname, min_choices, time_end, allowed_denied_choices, allow_search_visibility FROM surveys WHERE (closed=False AND deleted=False)"
            result = db.session.execute(text(sql))
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def save_survey_edit(self, survey_id, surveyname, survey_description, time_end):
        """
        SQL code for updating the values of a survey
        """
        try:
            sql = "UPDATE surveys SET surveyname=:surveyname, survey_description=:survey_description, time_end=:time_end WHERE id=:survey_id"
            db.session.execute(
                text(sql), {"survey_id": survey_id, "surveyname": surveyname, "survey_description": survey_description, "time_end": time_end}
            )
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_all_surveys(self):
        """
        SQL code for getting all surveys.
        """
        try:
            sql = "SELECT * FROM surveys"
            result = db.session.execute(text(sql))
            surveys = result.fetchall()
            if not surveys:
                return False
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def set_survey_deleted_true(self, survey_id):
        """
        SQL code for setting survey's deleted field true

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET deleted = True WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False


survey_repository = SurveyRepository()
