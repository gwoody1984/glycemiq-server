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
        self.send(self.myAddress, ActorExitRequest())

    def _save_activity(self, user_id, date, data):
        logger.debug(str(data))

        if not isinstance(data, dict):
            logger.error("Expected dict, got {}".format(str(type(data))))
            return

        summary_section = data['summary']

        activity = Activity()
        activity.receive_date = datetime.utcnow()
        activity.fitbit_user_id = user_id
        activity.date = date
        activity.steps = summary_section['steps']
        activity.resting_heart_rate = summary_section['restingHeartRate']
        activity.sedentary_minutes = summary_section['sedentaryMinutes']
        activity.lightly_active_minutes = summary_section['lightlyActiveMinutes']
        activity.fairly_active_minutes = summary_section['fairlyActiveMinutes']
        activity.very_active_minutes = summary_section['veryActiveMinutes']
        activity.calories_out = summary_section['caloriesOut']

        db.session.add(activity)
        db.session.commit()
