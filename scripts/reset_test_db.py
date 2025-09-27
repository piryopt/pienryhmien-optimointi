import os
from flask import Flask
from dotenv import load_dotenv
from src import db
from src.tools.db_tools import clear_database


def main():
    load_dotenv()
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
    db.init_app(app)
    with app.app_context():
        clear_database()
        print("Test database cleared.")


if __name__ == "__main__":
    main()
