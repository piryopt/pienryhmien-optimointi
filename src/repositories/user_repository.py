import os
from sqlalchemy import text
from src import db
from flask import current_app


class UserRepository:
    def find_by_email(self, email):
        """
        SQL code for getting all data from a user_survey_ranking entry

        args:
            user_id: The id of the user
            survey_id: The id of the survey
        """
        try:
            sql = "SELECT * FROM users WHERE email=:email"
            result = db.session.execute(text(sql), {"email": email})
            user = result.fetchone()
            return user
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def register(self, user):
        """
        SQL code for adding a new user into the database

        args:
            user: Contains all user data. Email, name, and True/False if teacher/student
        """
        existing_user = self.find_by_email(user.email)
        if existing_user:
            print(f"The user with the email {user.email} already exists!")
            return None
        try:
            # Only allow automatic dev admin granting when running in debug and when
            # DEV_ADMIN_NAME is explicitly set.
            admin_flag = False
            try:
                if current_app and current_app.debug and os.getenv("DEV_ADMIN_NAME"):
                    admin_flag = os.getenv("DEV_ADMIN_NAME") == user.name
            except RuntimeError:
                # no app context -> don't grant admin
                admin_flag = False

            sql = "INSERT INTO users (name, email, isteacher, admin, language) VALUES (:name, :email, :isteacher, :admin, :language)"
            db.session.execute(
                text(sql),
                {"name": user.name, "email": user.email, "isteacher": user.isteacher, "admin": admin_flag, "language": "fi"},
            )
            if user.isteacher:
                update_statistics_sql = """
                    UPDATE statistics SET registered_teachers_count = registered_teachers_count + 1 
                    WHERE is_current_row = TRUE
                """
            else:
                update_statistics_sql = """
                    UPDATE statistics SET registered_students_count = registered_students_count + 1 
                    WHERE is_current_row = TRUE
                """
            db.session.execute(text(update_statistics_sql))
            db.session.commit()
            # Reflect admin flag on returned entity so callers see it
            try:
                user.admin = admin_flag
            except Exception:
                pass
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None
        return user

    def get_all_students(self):
        """
        SQL code for getting a list of all students. Used for analytics in the admin page.
        """
        try:
            sql = "SELECT * FROM users WHERE isteacher=False"
            result = db.session.execute(text(sql))
            users = result.fetchall()
            return users
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_user_data(self, user_id):
        """
        SQL code for getting all data from a user

        args:
            user_id: The id of a user
        """
        try:
            sql = "SELECT * FROM users WHERE id=:id"
            result = db.session.execute(text(sql), {"id": user_id})
            user = result.fetchone()
            return user
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def make_user_teacher(self, email):  # don't remove, needed later
        """
        SQL code for giving a user teacher privileges

        args:
            email: The email of the user
        """
        sql = "UPDATE users SET isteacher=true WHERE email=:email"
        db.session.execute(text(sql), {"email": email})
        db.session.commit()

    def get_all_teachers(self):
        """
        SQL code for getting all teachers

        args:
            user_id: The id of a user
        """
        try:
            sql = "SELECT * FROM users WHERE isteacher=True"
            result = db.session.execute(text(sql))
            teachers = result.fetchall()
            return teachers
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return []

    def get_user_by_email(self, email):
        """
        SQL code for the id of a user with its email

        args:
            email: The email of a user
        """
        try:
            sql = "SELECT * FROM users WHERE email=:email"
            result = db.session.execute(text(sql), {"email": email})
            user = result.fetchone()
            return user
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return None

    def change_user_language(self, user_id, language):
        """
        SQL code for changing the default language of the user

        args:
            user_id: The id of a user
            language: The updated language
        """
        try:
            sql = "UPDATE users SET language=:language WHERE id=:user_id"
            db.session.execute(text(sql), {"user_id": user_id, "language": language})
            db.session.commit()
            return True
        except Exception as e:  # pylint: disable=W0718
            print(e)
            return False


user_repository = UserRepository()
