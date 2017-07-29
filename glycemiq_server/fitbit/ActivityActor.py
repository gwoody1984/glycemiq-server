from datetime import datetime

from thespian.actors import ActorExitRequest

from glycemiq_server.fitbit.FitbitDataActor import FitbitDataActor
from glycemiq_server.log_manager import logManager
from glycemiq_server.models import db, Activity

logger = logManager.get_logger(__name__)


class ActivityActor(FitbitDataActor):

    def receiveMessage(self, msg, sender):
        if not isinstance(msg, dict):
            return

        user_id = msg['ownerId']
        date = msg['date']

        self.server.set_fitbit_client(user_id)
        data = self.server.get_activities(user_id, date)

        self._save_activity(user_id, date, data)
        self.send(self, ActorExitRequest())

    def _save_activity(self, user_id, date, data):
        logger.debug(str(data))

        if not isinstance(data, dict):
            logger.error("Expected dict, got {}".format(str(type(data))))
            return

        summarySection = data['summary']

        activity = Activity()
        activity.receive_date = datetime.utcnow()
        activity.user_id = user_id
        activity.date = date
        activity.steps = summarySection['steps']
        activity.restingHeartRate = summarySection['restingHeartRate']
        activity.sedentaryMinutes = summarySection['sedentaryMinutes']
        activity.lightlyActiveMinutes = summarySection['lightlyActiveMinutes']
        activity.fairlyActiveMinutes = summarySection['fairlyActiveMinutes']
        activity.veryActiveMinutes = summarySection['veryActiveMinutes']
        activity.caloriesOut = summarySection['caloriesOut']

        db.session.add(activity)
        db.session.commit()

