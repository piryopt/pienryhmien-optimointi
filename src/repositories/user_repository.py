from sqlalchemy import text
from src import db

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
            result = db.session.execute(text(sql), {"email":email})
            user = result.fetchone()
            if not user:
                return False
            return user
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def register(self, user):
        """
        SQL code for adding a new user into the database

        args:
            user: Contains all user data. Email, name, and True/False if teacher/student
        """
        existing_user = self.find_by_email(user.email)
        if existing_user:
            print(f"The user with the email {user.email} already exists!")
            return
        try:
            sql = "INSERT INTO users (name, email, isteacher, admin, language)" \
                  "VALUES (:name, :email, :isteacher, False, :language) RETURNING id"
            result = db.session.execute(text(sql), {"name":user.name, "email":user.email, "isteacher":user.isteacher, "language":"fi"})
            user_id = result.fetchone()[0]
            sql = """
                UPDATE users
                SET name = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                       REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(
                       REPLACE(REPLACE(REPLACE(name, 'Ã¤', 'ä'), 'Ã¶', 'ö'), 'Ã¥', 'å'),
                       'Ã„', 'Ä'), 'Ã–', 'Ö'), 'Ã…', 'Å'), 'Ã©', 'é'), 'Ã¼', 'ü'),
                       'Ã ', 'à'), 'Ã«', 'ë'), 'Ãº', 'ú'), 'Ã³', 'ó'), 'Ã¡', 'á')
                WHERE id = :user_id
            """
            db.session.execute(text(sql), {"user_id":user_id})
            db.session.commit()
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        return user

    def get_all_students(self):
        """
        SQL code for getting a list of all students. Used for analytics in the admin page.
        """
        try:
            sql = "SELECT * FROM users WHERE isteacher=False"
            result = db.session.execute(text(sql))
            users = result.fetchall()
            if not users:
                return False
            return users
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

    def get_user_data(self, user_id):
        """
        SQL code for getting all data from a user

        args:
            user_id: The id of a user
        """
        try:
            sql = "SELECT * FROM users WHERE id=:id"
            result = db.session.execute(text(sql), {"id":user_id})
            user = result.fetchone()
            if not user:
                return False
            return user
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def make_user_teacher(self, email): # don't remove, needed later
        """
        SQL code for giving a user teacher privileges

        args:
            email: The email of the user
        """
        sql = "UPDATE users SET isteacher=true WHERE email=:email"
        db.session.execute(text(sql), {"email":email})
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
            if not teachers:
                return False
            return teachers
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def get_user_by_email(self, email):
        """
        SQL code for the id of a user with its email

        args:
            email: The email of a user
        """
        try:
            sql = "SELECT * FROM users WHERE email=:email"
            result = db.session.execute(text(sql), {"email":email})
            user = result.fetchone()
            if not user:
                return False
            return user
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def change_user_language(self, user_id, language):
        """
        SQL code for changing the default language of the user

        args:
            user_id: The id of a user
            language: The updated language
        """
        try:
            sql = "UPDATE users SET language=:language WHERE id=:user_id"
            db.session.execute(text(sql), {"user_id":user_id, "language":language})
            db.session.commit()
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

user_repository = UserRepository()
