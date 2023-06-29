from src import db
from flask_login import UserMixin

class NewUser(UserMixin, db.Model):
    __tablename__ = "new_users_table"
    name = db.Column(db.String)
    student_number = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    role = db.Column(db.String)

    def get_id(self):
        return self.student_number