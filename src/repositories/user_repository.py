from app import db
from sqlalchemy import text

class UserRepository:

    def find_by_email(self, email):
        try:
            sql = "SELECT * FROM dummyusers WHERE email=:email"
            result = db.session.execute(text(sql), {"email":email})
            user = result.fetchone()
            if not user:
                return False
            return user
        except:
            return False

    def register(self, user):
        existing_user = self.find_by_email(user.email)
        if existing_user:
            print(f"The user with the email {user.email} already exists!")
            return
        try:
            sql = "INSERT INTO dummyusers (firstname, lastname, student_number, email, password, isteacher) VALUES (:firstname, :lastname, :student_number, :email, :password, :isteacher)"
            db.session.execute(text(sql), {"firstname":user.firstname, "lastname":user.lastname, "student_number":user.student_number, "email":user.email, "password":user.password, "isteacher":user.isteacher})
            db.session.commit()
        except:
            print("ERROR WHEN ADDING NEW USER TO DB")
            return False
        return user

user_repository = UserRepository()
