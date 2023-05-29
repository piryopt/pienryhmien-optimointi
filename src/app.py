from flask import Flask, render_template
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from db_urls import DatabaseURL
import os

#import routes

app = Flask(__name__)

database_url = DatabaseURL()

username = database_url.get_user_production()
password = database_url.get_production_password()
port = database_url.get_port()
host = database_url.get_host()
database = database_url.get_database_production()


DATABASE_URL = "postgresql://" + username + ":" + password + "@" + host + ":" + str(port) + "/" + database

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
db = SQLAlchemy(app)

app.debug = True


@app.route("/db_connection_test")
def db_connection_test():
    run_query = db.session.execute(text('SELECT 1;'))
    result = run_query.fetchone()
    return str(result)


if __name__ == '__main__':
    app.run()
