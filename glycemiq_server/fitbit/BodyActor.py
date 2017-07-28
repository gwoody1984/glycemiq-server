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
        data = self.server.get_heart_rate(user_id, date)

        self._save_activity(data)
        self.send(self, ActorExitRequest())

    def _save_activity(self, data):
        logger.debug(str(data))
