from datetime import datetime

from thespian.actors import ActorExitRequest

from glycemiq_server.fitbit.FitbitDataActor import FitbitDataActor
from glycemiq_server.log_manager import logManager
from glycemiq_db import db, Activity

logger = logManager.get_logger(__name__)


class ActivityActor(FitbitDataActor):
    def receiveMessage(self, msg, sender):
        if not isinstance(msg, dict):
            return

        fitbit_user_id = msg['ownerId']
        glycemiq_user_id = msg['user']
        date = msg['date']

        self.server.set_fitbit_client(fitbit_user_id)
        data = self.server.get_activities(fitbit_user_id, date)

        self._save_activity(fitbit_user_id, glycemiq_user_id, date, data)
        self.send(self.myAddress, ActorExitRequest())

    @staticmethod
    def _save_activity(fitbit_user_id, glycemiq_user_id, date, data):
        logger.debug(str(data))

        if not isinstance(data, dict):
            logger.error("Expected dict, got {}".format(str(type(data))))
            return

        summary_section = data['summary']

        activity = Activity()
        activity.receive_date = datetime.utcnow()
        activity.fitbit_user_id = fitbit_user_id
        activity.user_id = glycemiq_user_id
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
