import os


class Config(object):
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY") or 'thisisasecret'


class TestingConfig(Config):
    DEBUG = True
