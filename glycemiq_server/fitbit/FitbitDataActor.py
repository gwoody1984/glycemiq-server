from thespian.actors import *

from glycemiq_server.config import config_as_dict
from glycemiq_server.fitbit.OAuth2Server import OAuth2Server


class FitbitDataActor(Actor):
    def __init__(self):
        super().__init__()
        config = config_as_dict('FITBIT')
        self.server = OAuth2Server(config['CLIENT_ID'], config['CLIENT_SECRET'])
