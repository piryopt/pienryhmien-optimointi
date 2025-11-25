from sqlalchemy import text  # pylint: disable=R0401
from src import db


class UserRankingsRepository:
    def add_user_ranking(self, user_id, survey_id, ranking, rejections, reason, ranking_exists):
        """
        SQL code for adding a new entry into user_survey_rankings table

        args:
            user_id: The id of the user
            survey_id: The id of the survey
            ranking: The ranking of the user for the survey in question
            rejections: The rejections of the user for the survey in question
            reason: The reason of the user for the rejections of the survey in question
            ranking_exists: Boolean of ranking existing
        """
        try:
            sql = """
                WITH updated AS (
                UPDATE user_survey_rankings
                SET ranking = :ranking,
                    rejections = :rejections,
                    reason = :reason,
                    deleted = :deleted
                WHERE user_id = :user_id
                  AND survey_id = :survey_id
                RETURNING id
                )
                INSERT INTO user_survey_rankings (user_id, survey_id, ranking, rejections, reason, deleted)
                SELECT :user_id, :survey_id, :ranking, :rejections, :reason, :deleted
                WHERE NOT EXISTS (SELECT 1 FROM updated);
                """
            db.session.execute(
                text(sql),
                {"user_id": user_id, "survey_id": survey_id, "ranking": ranking, "rejections": rejections, "reason": reason, "deleted": False},
            )
            
            if not ranking_exists:
                update_statistics_sql = """
                    UPDATE statistics SET total_survey_answers = total_survey_answers + 1 WHERE is_current_row = TRUE
                """
                db.session.execute(text(update_statistics_sql))

            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            if "Working outside of application context." not in str(e):
                db.session.rollback()
            return False

    def add_multistage_user_ranking(self, user_id, survey_id, ranking, rejections, reason, stage, not_available, ranking_exists):
        """
        SQL code for adding a new entry into user_survey_rankings table

        args:
            user_id: The id of the user
            survey_id: The id of the survey
            ranking: The ranking of the user for the survey in question
            rejections: The rejections of the user for the survey in question
            reason: The reason of the user for the rejections of the survey in question
        """
        try:
            sql = """
                INSERT INTO user_survey_rankings (user_id, survey_id, ranking, rejections, 
                    reason, deleted, stage, not_available) 
                VALUES (:user_id, :survey_id, :ranking, :rejections, :reason, :deleted,
                    :stage, :not_available) 
                ON CONFLICT (user_id, survey_id, stage) 
                DO UPDATE SET ranking=:ranking, rejections=:rejections, reason=:reason, deleted=:deleted,
                    stage=:stage, not_available=:not_available
                """
            db.session.execute(
                text(sql),
                {"user_id": user_id, "survey_id": survey_id, 
                 "ranking": ranking, "rejections": rejections, 
                 "reason": reason, "deleted": False,
                 "stage": stage, "not_available": not_available
                 },
            )
            if not ranking_exists:
                update_statistics_sql = """
                    UPDATE statistics SET total_survey_answers = total_survey_answers + 1 WHERE is_current_row = TRUE
                """
                db.session.execute(text(update_statistics_sql))
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            if "Working outside of application context." not in str(e):
                db.session.rollback()
            return False

    def get_user_ranking(self, user_id, survey_id):
        """
        SQL code for getting all data from a user_survey_ranking entry

        args:
            user_id: The id of the user
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT * FROM user_survey_rankings WHERE (user_id=:user_id AND survey_id=:survey_id AND deleted=False)"
            result = db.session.execute(text(sql), {"user_id": user_id, "survey_id": survey_id})
            ranking = result.fetchone()
            return ranking
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def get_user_multistage_rankings(self, survey_id, user_id):
        """
        Fetches user's multistage rankings for given survey.
        Returns all stages and their answers.
        """
        try:
            sql = """
                SELECT 
                usr.survey_id,
                usr.user_id,
                usr.stage,
                usr.ranking,
                usr.rejections,
                usr.reason,
                usr.not_available
                FROM user_survey_rankings usr
                LEFT JOIN survey_stages ss
                    ON usr.survey_id = ss.survey_id
                   AND usr.stage = ss.stage
                WHERE usr.survey_id = :survey_id
                  AND usr.user_id = :user_id
                  AND usr.deleted = FALSE
                ORDER BY ss.order_number NULLS LAST, usr.stage;
            """
            result = db.session.execute(text(sql), {"survey_id": survey_id, "user_id": user_id})
            return result.fetchall()
        except Exception as e:
            print(e)
            return []

    def user_ranking_exists(self, user_id, survey_id):
        """
        Returns boolean of a survey ranking existing for a user
        """
        try:
            sql = """
                SELECT EXISTS (SELECT 1 FROM user_survey_rankings
                WHERE user_id = :user_id AND survey_id = :survey_id AND deleted = FALSE)
            """
            result = db.session.execute(text(sql), {"user_id": user_id, "survey_id": survey_id})
            return result.fetchone()[0]
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False

    def delete_user_ranking(self, user_id, survey_id):
        """
        SQL code for deleting a user_survey_ranking entry. It can be manually restored if no new ranking is added

        args:
            user_id: The id of the user
            survey_id: The id of the survey
        """
        try:
            sql = "UPDATE user_survey_rankings SET deleted = True WHERE (user_id=:user_id AND survey_id=:survey_id)"
            db.session.execute(text(sql), {"user_id": user_id, "survey_id": survey_id})
            update_statistics_sql = """
                UPDATE statistics SET total_survey_answers = total_survey_answers - 1 WHERE is_current_row = TRUE
            """
            db.session.execute(text(update_statistics_sql))
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            if "Working outside of application context." not in str(e):
                db.session.rollback()
            return False
        
    def get_all_rankings(self):
        """
        SQL code for getting the amount of all rankings. Used for analytics in the admin page.
        """
        try:
            sql = "SELECT COUNT(id) FROM user_survey_rankings"
            result = db.session.execute(text(sql))
            rankings_count = result.fetchone()[0]
            return rankings_count
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return 0

    def get_all_rankings_by_stage(self, survey_id, stage):
        """
        SQL code for getting all rankings from a multistage survey by stage.
        """
        try:
            sql = """
            SELECT 
                user_id,
                ranking,
                rejections,
                reason,
                not_available
                FROM user_survey_rankings
                WHERE survey_id=:survey_id AND stage=:stage AND deleted = FALSE
            """
            result = db.session.execute(text(sql), {"survey_id": survey_id, "stage": stage})
            rankings = result.fetchall()
            return rankings
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []
        
    def get_user_multistage_rankings_by_stage(self, survey_id, user_id, stage):
        """
        SQL code for getting user rankings from a multistage survey stage
        """
        try:
            sql = """
            SELECT 
                ranking,
                rejections,
                reason,
                not_available
                FROM user_survey_rankings
                WHERE survey_id=:survey_id AND stage=:stage AND user_id=:user_id AND deleted = FALSE
            """
            result = db.session.execute(text(sql), {"survey_id": survey_id, "stage": stage, "user_id": user_id})
            rankings = result.fetchone()
            return rankings
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

user_rankings_repository = UserRankingsRepository()
