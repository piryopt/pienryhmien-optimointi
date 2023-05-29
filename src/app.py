from flask import Flask, render_template
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from db_urls import DatabaseURL
import routes

app = Flask(__name__)
app.debug = True

db = SQLAlchemy(app)


database_url = DatabaseURL()
DATABASE_URL_TEST = database_url.get_url("test")
DATABASE_URL_PRODUCTION = database_url.get_url("production")


app.config["SQLALCHEMY_DATABASE_URI"] = getenv(DATABASE_URL_PRODUCTION)

# TODO: entäs testikanta?

@app.route("/")
def hello_world() -> str:
    """
    Returns the rendered skeleton template
    """
    return render_template('index.html')

def db_connection_test():
    """
    Tests db-connection. 
    """


