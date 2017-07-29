from thespian.actors import ActorExitRequest

from glycemiq_server.fitbit.FitbitDataActor import FitbitDataActor
from glycemiq_server.log_manager import logManager

logger = logManager.get_logger(__name__)


class BodyActor(FitbitDataActor):

    def receiveMessage(self, msg, sender):
        if not isinstance(msg, dict):
            return

        user_id = msg['ownerId']
        date = msg['date']

        self.server.set_fitbit_client(user_id)
        bmi_data = self.server.get_bmi(user_id, date)
        body_fat_data = self.server.get_body_fat_percent(user_id, date)
        weight_data = self.server.get_weight(user_id, date)

        self._save_body_data(user_id, date, bmi_data, body_fat_data, weight_data)
        self.send(self, ActorExitRequest())

    def _save_body_data(self, user_id, date, bmi, body_fat, weight):
        logger.debug('bmi: ' + str(bmi))
        logger.debug('body fat: ' + str(body_fat))
        logger.debug('weight: ' + str(weight))
