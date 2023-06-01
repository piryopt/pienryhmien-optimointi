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


# TOIMII
conn_info = DatabaseURL()
TESTDATABASE_URL = "postgresql://" + conn_info.get_user_test() + ":" + conn_info.get_test_password() + "@" + conn_info.get_host() +  ":5432/" + conn_info.get_database_test() + "?ssl=true"


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
