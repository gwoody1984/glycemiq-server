import configparser
import json
import os

config = configparser.ConfigParser()

if os.path.exists('config.json'):
    with open('config.json', 'r') as file:
        config = json.load(file)

def config_section(section):
    return config[section]