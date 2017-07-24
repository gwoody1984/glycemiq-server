import os
import configparser

config = configparser.ConfigParser()
basedir = os.path.abspath(os.path.dirname(__file__))


class DevelopmentConfig():
    DEBUG = True

    with open('config.json')


class ProductionConfig():
    DEBUG = False


config_by_env = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
)
