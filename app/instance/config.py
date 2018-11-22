import os


class Config(object):
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY") or 'thisisasecret'
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(Config):
    DEBUG = True
