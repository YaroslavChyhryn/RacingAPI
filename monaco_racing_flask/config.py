import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = 'sqlite:///' + os.path.join(basedir, 'monaco_racing.db')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    DATABASE = 'sqlite:///' + os.path.join(basedir, 'test_monaco_racing.db')


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
