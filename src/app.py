from flask import Flask, session
from tools import hospital_data_gen
from flask_sqlalchemy import SQLAlchemy
form os import getenv

app = Flask(__name__)

db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

import routes

def db_connection_test():
    """
    Tests db-connection. 
    """
