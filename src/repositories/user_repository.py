from sqlalchemy import text
from src import db

class UserRepository:

    def find_by_email(self, email):
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
        existing_user = self.find_by_email(user.email)
        if existing_user:
            print(f"The user with the email {user.email} already exists!")
            return
        try:
            sql = "INSERT INTO users (name, student_number, email, isteacher)" \
                  "VALUES (:name, :student_number, :email, :isteacher)"
            db.session.execute(text(sql), {"name":user.name,"student_number":user.student_number,
                                            "email":user.email, "isteacher":user.isteacher})
            db.session.commit()
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        return user
    
    def get_all_users(self):
        try:
            sql = "SELECT * FROM users"
            result = db.session.execute(text(sql))
            users = result.fetchall()
            if not users:
                return False
            return users
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False
        
    def get_user_data(self, id):
        try:
            sql = "SELECT * FROM users WHERE id=:id "
            result = db.session.execute(text(sql), {"id":id})
            user = result.fetchone()
            if not user:
                return False
            return user
        except Exception as e: # pylint: disable=W0718
            print(e)
            return False

user_repository = UserRepository()
