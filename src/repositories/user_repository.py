from app import db
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash

class UserRepository:

    def find_by_email(self, email, password):
        try:
            sql = "SELECT * FROM users WHERE email=:email"
            result = db.session.execute(text(sql), {"email":email})
            user = result.fetchone()
            if not user:
                return False
            if check_password_hash(user.password, password):
                return user
            return False
        except:
            return False

    def register(self, user):
        existing_user = self.find_by_email(user.email, user.password)
        if existing_user:
            print(f"The user with the email {user.email} already exists!")
            return
        hash_value = generate_password_hash(user.password)
        try:
            sql = "INSERT INTO users (firstname, lastname, student_number, email, password, isteacher) VALUES (:firstname, :lastname, :student_number, :email, :password, :isteacher)"
            db.session.execute(text(sql), {"firstname":user.firstname, "lastname":user.lastname, "student_number":user.student_number, "email":user.email, "password":hash_value, "isteacher":user.isteacher})
            db.session.commit()
        except:
            print("ERROR WHEN ADDING NEW USER TO DB")
            return False
        return user

user_repository = UserRepository()
