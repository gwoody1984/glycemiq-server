import ast

from thespian.actors import *

from ..log_manager import logManager


logger = logManager.get_logger(__name__)


class NotificationActor(Actor):
    # def __init__(self, oauth_server):
    #     self.server = oauth_server

    def receiveMessage(self, msg, sender):
        if isinstance(msg, ActorExitRequest):
            return

        logger.debug(str(msg))
        self.send(self.myAddress, ActorExitRequest())

