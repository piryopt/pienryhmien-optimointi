from flask import Flask, render_template
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_urls import DatabaseURL

#import routes

app = Flask(__name__)

database_url = DatabaseURL()

username = database_url.get_user_production()
password = database_url.get_production_password()
port = database_url.get_port()
host = database_url.get_host()
path = database_url.get_path()
database = database_url.get_database_production()

# EI TOIMI VIELÄ!!
DATABASE_URL = "postgresql+psycopg2://" + username + ":" + password + "@" + host + ":" + str(port) + path + "/" + database

print(DATABASE_URL)

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

db = SQLAlchemy(app)

app.debug = True


@app.route("/db_connection_test")
def db_connection_test():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    run_query = db.session.execute(text('SELECT 1;'))
    result = run_query.fetchone()
    return str(result)


if __name__ == '__main__':
    app.run()
