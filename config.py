import os

# default config


class BaseConfig(object):
    DEBUG = False
    TESTING = False
    # shortened for readability
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///../../db/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = True
    DEBUG = False
    LOGIN_DISABLED = True
