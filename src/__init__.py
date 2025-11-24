import os
from flask import Flask, session
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from dotenv import load_dotenv
from src.tools.date_converter import format_datestring
from flask_cors import CORS


csfr = CSRFProtect()
db = SQLAlchemy()
babel = Babel()
scheduler = APScheduler()


class Config:
    SCHEDULER_API_ENABLED = True
    BABEL_DEFAULT_LOCALE = "fi"


def get_locale():
    from flask import has_request_context

    if not has_request_context():
        return "fi"
    lang = session.get("language")
    if isinstance(lang, str) and lang:
        return lang
    return "fi"


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__, static_folder="./static/react", static_url_path="/")
    CORS(app, origins=["http://localhost:5173", "http://localhost:5001"], supports_credentials=True)

    # app.config.from_object(Config())
    app.config.setdefault("SESSION_COOKIE_HTTPONLY", True)

    if os.getenv("FLASK_USE_SECURECOOKIES", "0") == "1":
        app.config["SESSION_COOKIE_SECURE"] = True
        app.config["SESSION_COOKIE_SAMESITE"] = "None"
    else:
        app.config["SESSION_COOKIE_SECURE"] = False
        app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    env = os.getenv("FLASK_ENV", "development")
    app.config["ENV"] = env

    if test_config is None:
        if env == "testing":
            app.config["SECRET_KEY"] = os.getenv("TEST_SECRET_KEY")
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("TEST_DATABASE_URL")
        else:
            app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

        app.config["DEBUG"] = os.getenv("FLASK_DEBUG", "0") == "1"

    else:
        app.config.update(test_config)

    csfr.init_app(app)
    db.init_app(app)
    babel.init_app(app, locale_selector=get_locale)

    if test_config is None or env != "testing":
        # initialize scheduler if not running tests

        from src.routes import close_surveys, delete_old_surveys, delete_trashed_surveys, save_old_statistics

        scheduler.init_app(app)
        scheduler.start()

        @scheduler.task("cron", id="close_surveys", minute=0)
        def scheduled_close_surveys():
            with app.app_context():
                close_surveys()

        @scheduler.task("cron", id="delete_old_surveys", hour=0, minute=0)
        def scheduled_delete_trashed_surveys():
            with app.app_context():
                delete_trashed_surveys()

        @scheduler.task("cron", id="delete_old_surveys", day_of_week="mon", hour=0, minute=0)
        def scheduled_delete_old_surveys():
            with app.app_context():
                delete_old_surveys()

        @scheduler.task("cron", id="save_old_statistics", day_of_week="mon", hour=0, minute=0)
        def scheduled_save_old_statistics():
            with app.app_context():
                save_old_statistics()

    # make format_datestring accessible from jinja templates
    app.jinja_env.globals.update(format_datestring=format_datestring)

    from src.routes import bp

    app.register_blueprint(bp)

    return app


app = create_app()
