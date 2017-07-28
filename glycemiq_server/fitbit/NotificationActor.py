from datetime import datetime

from thespian.actors import *

from glycemiq_server.models import db, Notification
from glycemiq_server.log_manager import logManager
from glycemiq_server.fitbit.ActivityActor import ActivityActor
from glycemiq_server.fitbit.BodyActor import BodyActor
from glycemiq_server.fitbit.FoodActor import FoodActor
from glycemiq_server.fitbit.SleepActor import SleepActor

logger = logManager.get_logger(__name__)


class NotificationActor(Actor):
    def __init__(self):
        super().__init__()
        self.children = {
            'foods': FoodActor,
            'activities': ActivityActor,
            'sleep': SleepActor,
            'body': BodyActor
        }

    def receiveMessage(self, msg, sender):
        if not isinstance(msg, list):
            return

        logger.debug(str(msg))
        msg['date'] = datetime.strptime(msg['date'], "%Y-%m-%d").date()
        msg['subscriptionId'] = int(msg['subscriptionId'])

        for item in msg:
            self._route_message(item)

    def _route_message(self, msg):
        child_type = self.children[msg['collectionType']]
        if child_type is not None:
            child_actor = self.createActor(child_type)
            self.send(child_actor, msg)

    def _save_notification(self, msg):
        notification = Notification()
        notification.receive_date = datetime.utcnow()
        notification.collection_Type = msg['collectionType']
        notification.user_id = msg['ownerId']
        notification.date = msg['date']
        notification.owner_type = msg['ownerType']
        notification.subscription_id = msg['subscriptionId']

        db.session.add(notification)
        db.session.commit()
