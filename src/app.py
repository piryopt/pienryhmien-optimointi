from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.debug = True

#db = SQLAlchemy(app)
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

import routes

'''def db_connection_test():
    """
    Tests db-connection. 
    """'''
