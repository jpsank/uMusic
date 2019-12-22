import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'you-will-never-guess'
    SESSION_TYPE = 'sqlalchemy'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMINS = ['julian@sankergroup.org']

    SENTRY_DSN = None

    TRACKS_PER_PAGE = 56

    SOUNDCLOUD_CLIENT_ID = "YUKXoArFcqrlQn9tfNHvvyfnDISj04zk"
    SOUNDCLOUD_FOLDER = os.path.join(basedir, 'app/static/soundcloud/')
    SOUNDCLOUD_IMAGE_FOLDER = os.path.join(basedir, 'app/static/sd_cover_art/')

