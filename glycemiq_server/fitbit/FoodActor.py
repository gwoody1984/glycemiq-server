from thespian.actors import ActorExitRequest

from glycemiq_server.fitbit.FitbitDataActor import FitbitDataActor
from glycemiq_server.log_manager import logManager

logger = logManager.get_logger(__name__)


class FoodActor(FitbitDataActor):
    """
    Not currently being used to retrieve data
    """

    def receiveMessage(self, msg, sender):
        if not isinstance(msg, dict):
            return

        logger.debug("ignoring food messages")
        self.send(self.myAddress, ActorExitRequest())
