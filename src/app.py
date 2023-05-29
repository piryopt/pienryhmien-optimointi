from flask import Flask, render_template
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from db_urls import DatabaseURL
import routes

app = Flask(__name__)
app.debug = True

db = SQLAlchemy(app)


database_url = DatabaseURL()

string_template = "postgresql://{username}:{password}@{host}:{port}/{database}"
DATABASE_URL = string_template.format(database_url.get_user_production, database_url.get_production_password, database_url.get_host, database_url.get_port, database_url.get_database_production)

#DATABASE_URL_TEST = database_url.get_url("test")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

# TODO: entäs testikanta?

import routes

'''def db_connection_test():
    """
    Tests db-connection. 
    """'''
