import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = 'postgresql:///playground'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'lumen'
    # FLASK_ADMIN_SWATCH = 'united'
