import ast

from thespian.actors import *


class NotificationActor(Actor):
    def __init__(self, oauth_server):
        self.server = oauth_server

    def receiveMessage(self, msg, sender):
        print(ast.literal_eval(msg))
