import configparser
import json
import os

config = configparser.ConfigParser()
basedir = os.path.abspath(os.path.dirname(__file__))
jsonConfig = os.path.join(basedir, 'config.json')

if os.path.exists(jsonConfig):
    with open(jsonConfig, 'r') as file:
        config = json.load(file)

def config_as_dict(section):
    return dict(config.get(section))