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

import config
from config import basedir


# Create application
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)
app.config.from_pyfile('config.py')

# Initialize Sentry if possible
if app.config['SENTRY_DSN']:
    sentry_sdk.init(
        dsn=app.config['SENTRY_DSN'],
        integrations=[FlaskIntegration(), SqlalchemyIntegration()]
    )
# Initialize folders
if not os.path.exists(app.config['SOUNDCLOUD_FOLDER']):
    os.mkdir(app.config['SOUNDCLOUD_FOLDER'])
if not os.path.exists(app.config['SOUNDCLOUD_IMAGE_FOLDER']):
    os.mkdir(app.config['SOUNDCLOUD_IMAGE_FOLDER'])


# Set up Flask modules

db = SQLAlchemy(app)

app.config['SESSION_SQLALCHEMY'] = db
sess = Session(app)

migrate = Migrate(app, db)
bootstrap = Bootstrap(app)
moment = Moment(app)


# Blueprints

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.main import bp as main_bp
app.register_blueprint(main_bp)


# Set logging

if not app.debug and not app.testing:
    if not os.path.exists(app.config['LOGS_PATH']):
        os.mkdir(app.config['LOGS_PATH'])
    file_handler = RotatingFileHandler(os.path.join(app.config['LOGS_PATH'], 'umusic.log'),
                                       maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('uMusic startup')


from app import models
