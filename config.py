import os

import settings

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SAMESITE = "None"
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = settings.db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = settings.admin_swatch
    TEMPLATE_MODE = settings.template_mode
    LOG_WITH_GUNICORN = settings.log_with_gunicorn


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
