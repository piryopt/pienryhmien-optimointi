from flask import Flask, render_template
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_urls import DatabaseURL
import psycopg2

#import routes

app = Flask(__name__)

database_url = DatabaseURL()

'''
username = database_url.get_user_production()
password = database_url.get_production_password()
port = database_url.get_port()
host = database_url.get_host()
path = database_url.get_path()
database = database_url.get_database_production()

# EI TOIMI VIELÄ!!
DATABASE_URL = "postgresql+psycopg2://" + username + ":" + password + "@" + host + ":" + str(port) + path + "/" + database
'''

# TOIMII
conn_info = DatabaseURL()
TESTDATABASE_URL = "postgresql://" + conn_info.get_user_test() + ":" + conn_info.get_test_password() + "@" + conn_info.get_host() +  ":5432/" + conn_info.get_database_test() + "?ssl=true"

#print(DATABASE_URL)

#app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

#db = SQLAlchemy(app)

app.debug = True


@app.route("/db_connection_test")
def db_connection_test():
    try:
        connection_uri = TESTDATABASE_URL
        print(connection_uri)
        conn = psycopg2.connect(connection_uri)
        conn.close()
    except Exception as e:
        print(e)


#
@app.route("/")
def results():

    # For testings only - later to be replaced with sorting algorithm function call
    results = [["Maija Mehiläinen", 12345, "ryhmä 1"],
               ["Matti Mehiläinen", 12346, "ryhmä 2"],
               ["Minna Mehiläinen", 12347, "ryhmä 3"]]

    return render_template("results.html", results=results)


if __name__ == '__main__':
    app.run()
