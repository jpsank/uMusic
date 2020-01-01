import os
basedir = os.path.abspath(os.path.dirname(__file__))


# Configuration

SESSION_TYPE = 'sqlalchemy'

LOGS_PATH = os.path.join(basedir, 'logs')

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

ADMINS = ['julian@sankergroup.org']

TRACKS_PER_PAGE = 56

SOUNDCLOUD_FOLDER = os.path.join(basedir, 'app/static/soundcloud/')
SOUNDCLOUD_IMAGE_FOLDER = os.path.join(basedir, 'app/static/sd_cover_art/')

