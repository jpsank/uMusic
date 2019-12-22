import logging
from logging.handlers import RotatingFileHandler
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_moment import Moment

from config import Config, basedir


if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration(), SqlalchemyIntegration()]
    )
if not os.path.exists(Config.SOUNDCLOUD_FOLDER):
    os.mkdir(Config.SOUNDCLOUD_FOLDER)
if not os.path.exists(Config.SOUNDCLOUD_IMAGE_FOLDER):
    os.mkdir(Config.SOUNDCLOUD_IMAGE_FOLDER)


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)

if not app.debug and not app.testing:
    logs_path = os.path.join(basedir, 'logs')
    if not os.path.exists(logs_path):
        os.mkdir(logs_path)
    file_handler = RotatingFileHandler(os.path.join(logs_path, 'umusic.log'),
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('uMusic startup')


from app import models
