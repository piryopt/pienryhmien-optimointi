import os
from flask import Flask
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

db = SQLAlchemy(app)

# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# make format_datestring accessible from jinja templates
from src.tools.date_converter import format_datestring
app.jinja_env.globals.update(format_datestring=format_datestring)

from src import routes
