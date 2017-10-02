from datetime import datetime

import dateutil.parser
from thespian.actors import ActorExitRequest

from glycemiq_server.fitbit.FitbitDataActor import FitbitDataActor
from glycemiq_server.log_manager import logManager
from glycemiq_server.models import db, SleepSummary, SleepDetail

logger = logManager.get_logger(__name__)


class SleepActor(FitbitDataActor):
    def receiveMessage(self, msg, sender):
        if not isinstance(msg, dict):
            return

        fitbit_user_id = msg['ownerId']
        glycemiq_user_id = msg['user']
        date = msg['date']

        self.server.set_fitbit_client(fitbit_user_id)
        data = self.server.get_sleep(fitbit_user_id, date)

        self._save_sleep(fitbit_user_id, glycemiq_user_id, date, data)
        self.send(self.myAddress, ActorExitRequest())

    def _save_sleep(self, fitbit_user_id, glycemiq_user_id, date, data):
        logger.debug(str(data))

        sleep_list = data['sleep']
        for item in sleep_list:
            sleep = self._create_sleep(fitbit_user_id, glycemiq_user_id, date, item)
            self._create_sleep_details(sleep, item['levels']['data'])

        db.session.commit()

    @staticmethod
    def _create_sleep(fitbit_user_id, glycemiq_user_id, date, sleep_summary):
        sleep = SleepSummary()
        sleep.receive_date = datetime.utcnow()
        sleep.date = date
        sleep.fitbit_user_id = fitbit_user_id
        sleep.user_id = glycemiq_user_id
        sleep.start_time = dateutil.parser.parse(sleep_summary['startTime'])
        sleep.end_time = dateutil.parser.parse(sleep_summary['endTime'])
        sleep.duration = sleep_summary['duration']
        sleep.efficiency = sleep_summary['efficiency']
        sleep.minutes_asleep = sleep_summary['minutesAsleep']
        sleep.minutes_awake = sleep_summary['minutesAwake']
        sleep.is_main_sleep = sleep_summary['isMainSleep']

        db.session.add(sleep)
        return sleep

    @staticmethod
    def _create_sleep_details(sleep, sleep_details):
        for item in sleep_details:
            detail = SleepDetail()
            detail.sleep_summary = sleep
            detail.data_point_time = dateutil.parser.parse(item['dateTime'])
            detail.level = item['level']
            detail.seconds = item['seconds']

            db.session.add(detail)
