import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig():
    DEBUG = True


class ProductionConfig():
    DEBUG = False


config_by_env = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
)
