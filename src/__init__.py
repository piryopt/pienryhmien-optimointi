import os
from flask import Flask, session
from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_babel import Babel
from dotenv import load_dotenv
from src.tools.date_converter import format_datestring


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
    return session.get("language", 0)


def create_app(test_config=None):
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config())

    env = os.getenv("FLASK_ENV", "development")

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

        from src.routes import close_surveys

        scheduler.init_app(app)
        scheduler.start()

        @scheduler.task("cron", id="close_surveys", hour="*")
        def scheduled_close_surveys():
            with app.app_context():
                close_surveys()

    # make format_datestring accessible from jinja templates
    app.jinja_env.globals.update(format_datestring=format_datestring)

    from src.routes import bp

    app.register_blueprint(bp)

    return app


app = create_app()
