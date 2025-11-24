import json
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
            return survey
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def is_multistage(self, survey_id):
        """
        SQL code for checking whether or not a survey is multistage

        args:
            survey_id: The id of the survey

        returns
            True if the survey is multistage, False otherwise
        """
        try:
            sql = "SELECT EXISTS (SELECT 1 FROM survey_stages ss WHERE ss.survey_id = :survey_id) AS is_multistage"
            result = db.session.execute(text(sql), {"survey_id": survey_id})
            row = result.fetchone()
            if not row:
                return False
            return bool(row[0])
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def is_multistage(self, survey_id):
        """
        SQL code for checking whether or not a survey is multistage

        args:
            survey_id: The id of the survey

        returns
            True if the survey is multistage, False otherwise
        """
        try:
            sql = "SELECT EXISTS (SELECT 1 FROM survey_stages ss WHERE ss.survey_id = :survey_id) AS is_multistage"
            result = db.session.execute(text(sql), {"survey_id": survey_id})
            row = result.fetchone()
            if not row:
                return False
            return bool(row[0])
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

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
        # Here we display all surveys created by a user that are not deleted, so in surveys table deleted=False
        try:
            sql = "SELECT COUNT(s.id) FROM surveys s, survey_owners so WHERE (so.user_id=:user_id AND so.survey_id=s.id AND s.deleted=False)"
            result = db.session.execute(text(sql), {"user_id": user_id})
            count = result.fetchone()
            if not count:
                return False
            return count.count
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
            update_statistics_sql = "UPDATE statistics SET active_surveys_count = active_surveys_count - 1 WHERE is_current_row = TRUE"
            db.session.execute(text(update_statistics_sql))
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            db.session.rollback()
            return False

    def open_survey(self, survey_id, new_end_time):
        """
        SQL code for opening a survey

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET closed = False, time_end = :new_end_time WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id, "new_end_time": new_end_time})
            update_statistics_sql = "UPDATE statistics SET active_surveys_count = active_surveys_count + 1 WHERE is_current_row = TRUE"
            db.session.execute(text(update_statistics_sql))
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            db.session.rollback()
            return False

    def get_active_surveys(self, user_id):
        """
        SQL code getting the list of all active surveys for which the user has access to.

        args:
            user_id: The id of the user
        """
        try:
            sql = """
                SELECT s.id, s.surveyname, s.time_end,
                EXISTS (SELECT 1 FROM survey_stages ss WHERE ss.survey_id = s.id)
                    AS is_multistage FROM surveys s, survey_owners so
                WHERE (so.user_id=:user_id AND closed=False AND s.id=so.survey_id AND s.deleted=False)
                """
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_active_surveys_and_response_count(self, user_id):
        """
        Get all active surveys and response counts to surveys where user is an owner.

        args:
            user_id: The id of the user
        """
        try:
            sql = """
            SELECT s.id, s.surveyname, s.time_end, 
            COUNT(DISTINCT CASE WHEN us.deleted = FALSE THEN us.user_id END) AS response_count,
            EXISTS (
                SELECT 1 FROM survey_stages ss WHERE ss.survey_id = s.id
            ) AS is_multistage FROM surveys s
            JOIN survey_owners so ON s.id = so.survey_id
            LEFT JOIN user_survey_rankings us ON s.id = us.survey_id
            WHERE (so.user_id=:user_id AND closed=False AND s.id=so.survey_id AND s.deleted=False)
            GROUP BY s.id, s.surveyname"""

            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()

            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_closed_surveys(self, user_id):
        """
        SQL code getting the list of all closed surveys for which the owner has access to.

        args:
            user_id: The id of the user
        """
        try:
            sql = """
                SELECT s.id, s.surveyname, s.closed, s.results_saved, s.time_end,
                EXISTS (SELECT 1 FROM survey_stages ss WHERE ss.survey_id = s.id)
                    AS is_multistage FROM surveys s, survey_owners so
                WHERE (so.user_id=:user_id AND s.closed=True AND so.survey_id = s.id AND s.deleted=False)
                ORDER BY s.time_end DESC
                """
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

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

    def create_new_survey(
        self,
        surveyname,
        min_choices,
        description,
        enddate,
        allowed_denied_choices=0,
        allow_search_visibility=True,
        allow_absences=False,
        user_id=None,
        min_choices_per_stage=None,
    ):
        """
        Creates a new survey, updates just surveys table
        RETURNS created survey's id
        """
        try:
            id = generate_unique_id(10)
            while self.get_survey(id):
                id = generate_unique_id(10)

            sql = """
                INSERT INTO surveys (id, surveyname, min_choices, min_choices_per_stage, closed,
                results_saved, survey_description, time_end, allowed_denied_choices, allow_search_visibility,
                allow_absences, deleted) VALUES (:id, :surveyname, :min_choices, :min_choices_per_stage, 
                :closed, :saved, :desc, :t_e, :a_d_c, :a_s_v, :a_a, False) RETURNING id
                """
            result = db.session.execute(
                text(sql),
                {
                    "id": id,
                    "surveyname": surveyname,
                    "min_choices": min_choices,
                    "min_choices_per_stage": json.dumps(min_choices_per_stage) if min_choices_per_stage is not None else None,
                    "closed": False,
                    "saved": False,
                    "desc": description,
                    "t_e": enddate,
                    "a_d_c": allowed_denied_choices,
                    "a_s_v": allow_search_visibility,
                    "a_a": allow_absences,
                },
            )
            update_statistics_sql = """
                UPDATE statistics SET total_created_surveys = total_created_surveys + 1,
                active_surveys_count = active_surveys_count + 1
                WHERE is_current_row = TRUE
            """
            db.session.execute(text(update_statistics_sql))
            db.session.commit()
            return result.fetchone()[0]
        except Exception as e:  # pylint: disable=W0718
            print(e)
            db.session.rollback()
            return None

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
            return None

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
            return None

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
            return None

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
            return None

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
            return None

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
            sql = text("SELECT user_id, ranking, rejections, reason FROM user_survey_rankings WHERE survey_id=:survey_id AND deleted IS FALSE")
            result = db.session.execute(sql, {"survey_id": survey_id})
            responses = result.fetchall()
            return responses
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def fetch_survey_responses_grouped_by_stages(self, survey_id):
        """Returns survey answers grouped by stage (grouping done in SQL)."""
        try:
            sql = text(
                "SELECT stage, user_id, ranking, rejections, reason "
                "FROM user_survey_rankings "
                "WHERE survey_id = :survey_id AND deleted IS FALSE "
                "ORDER BY stage, user_id"
            )
            result = db.session.execute(sql, {"survey_id": survey_id})
            rows = result.fetchall()

            grouped = {}
            for stage, user_id, ranking, rejections, reason in rows:
                grouped.setdefault(stage, []).append((user_id, ranking, rejections, reason))

            return grouped
        except Exception as e:
            print(e)
            return {}

    def fetch_survey_response_grouped_by_stages(self, survey_id):
        """Returns survey answers grouped by stage (grouping done in SQL)."""
        try:
            sql = text(
                "SELECT stage, user_id, ranking, rejections, reason, not_available "
                "FROM user_survey_rankings "
                "WHERE survey_id = :survey_id AND deleted IS FALSE "
                "ORDER BY stage, user_id"
            )
            result = db.session.execute(sql, {"survey_id": survey_id})
            rows = result.fetchall()

            grouped = {}
            for stage, user_id, ranking, rejections, reason, not_available in rows:
                grouped.setdefault(stage, []).append((user_id, ranking, rejections, reason, not_available))

            return grouped
        except Exception as e:
            print(e)
            return {}

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
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

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
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_all_active_surveys(self):
        """
        SQL code for getting all active surveys. Needed for automatic closing which will be checked every hour.
        """
        try:
            sql = "SELECT * FROM surveys WHERE (closed=False AND deleted=False)"
            result = db.session.execute(text(sql))
            surveys = result.fetchall()
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

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
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def set_survey_deleted_true(self, survey_id):
        """
        SQL code for setting survey's deleted field true

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET deleted = True, deleted_at = NOW() WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def set_survey_deleted_false(self, survey_id):
        """
        SQL code for setting survey's deleted field false

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE surveys SET deleted = False, deleted_at = NULL WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def delete_survey_permanently(self, survey_id):
        """
        SQL code for deleting survey and all related data permanently.

        args:
            survey_id: The id of the survey
        """
        try:
            sql = "DELETE FROM surveys WHERE id=:survey_id"
            db.session.execute(text(sql), {"survey_id": survey_id})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_all_survey_stages(self, survey_id):
        """
        SQL code for getting all survey stages.
        """
        try:
            sql = """
                    SELECT DISTINCT stage, order_number
                    FROM survey_stages
                    WHERE survey_id=:survey_id
                    ORDER BY order_number;
                """
            result = db.session.execute(text(sql), {"survey_id": survey_id})
            stages = result.fetchall()
            return stages
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_trash_count(self, user_id):
        """
        SQL code for getting the number of surveys in trash bin the owner has access to

        args:
            user_id: The id of the user
        """
        try:
            sql = "SELECT COUNT(s.id) FROM surveys s, survey_owners so WHERE (so.user_id=:user_id AND so.survey_id=s.id AND s.deleted=True)"
            result = db.session.execute(text(sql), {"user_id": user_id})
            count = result.fetchone()
            if not count:
                return False
            return count.count
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def get_deleted_surveys(self, user_id):
        """
        SQL code getting the list of all set to be deleted surveys for which the user has access to.

        args:
            user_id: The id of the user
        """
        try:
            sql = """
                SELECT s.id, s.surveyname, s.closed, s.deleted_at,
                EXISTS (SELECT 1 FROM survey_stages ss WHERE ss.survey_id = s.id)
                    AS is_multistage FROM surveys s, survey_owners so
                WHERE (so.user_id=:user_id AND s.id=so.survey_id AND s.deleted=True)
                """
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_all_deleted_surveys(self):
        """
        SQL code getting the list of all set to be deleted surveys.
        """
        try:
            sql = "SELECT s.id, s.surveyname, s.closed, s.deleted_at FROM surveys WHERE (deleted=True)"
            result = db.session.execute(text(sql), {"user_id": user_id})
            surveys = result.fetchall()
            return surveys
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_admintools_statistics(self):
        """
        SQL code for getting the admintools statistics
        """
        try:
            sql = """
                SELECT total_created_surveys, active_surveys_count, registered_teachers_count,
                registered_students_count, total_survey_answers FROM statistics WHERE is_current_row = TRUE
            """
            result = db.session.execute(text(sql))
            return result.fetchone()
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

survey_repository = SurveyRepository()
