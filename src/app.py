from flask import Flask, render_template
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#db = SQLAlchemy(app)
#app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

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


