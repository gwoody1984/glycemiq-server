from thespian.actors import ActorExitRequest

from glycemiq_server.fitbit.FitbitDataActor import FitbitDataActor
from glycemiq_server.log_manager import logManager

logger = logManager.get_logger(__name__)


class SleepActor(FitbitDataActor):

    def receiveMessage(self, msg, sender):
        if not isinstance(msg, dict):
            return

        user_id = msg['ownerId']
        date = msg['date']

        self.server.set_fitbit_client(user_id)
        data = self.server.get_sleep(user_id, date)

        self._save_sleep(user_id, date, data)
        self.send(self, ActorExitRequest())

    def _save_sleep(self, user_id, date, data):
        logger.debug(str(data))
