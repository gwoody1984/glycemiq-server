from fitbit.api import Fitbit

from glycemiq_server import db
from glycemiq_server.models import FitbitToken


class OAuth2Server:

    def __init__(self, client_id, client_secret, redirect_uri=None):
        """ Initialize the FitbitOauth2Client """
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

        self._fitbit = Fitbit(
            client_id,
            client_secret,
            redirect_uri=redirect_uri,
            timeout=10,
        )

    def set_fitbit_client(self, user_id):
        """
        Set client token properties for data requests

        :param user_id: Fitbit user_id sent back from authorization process.
        :type user_id: String
        """
        client_token = FitbitToken.query.filter_by(user_id=user_id).first()

        access_token = client_token.access_token
        refresh_token = client_token.refresh_token
        expires_at = client_token.expires_at

        self._fitbit = Fitbit(
            self._client_id,
            self._client_secret,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            refresh_cb=self._update_token
        )

    def fetch_access_token(self, code):
        """
        Once the user has agreed to provide Fitbit data to the application, this method will use the
        authorization code passed back from that process to retrieve the user's access token information

        :param code: Authorization code sent to the application after the user has authorize the use of Fitbit data.
        :type code: String
        :return: An access token for the user.
        :rtype: OAuth2Token
        """
        token = self._fitbit.client.fetch_access_token(code)
        self._update_token(token)

        return token

    def subscribe(self, user_id):
        """
        Allows the app to begin receiving push updates when a user syncs their Fitbit device

        :param user_id: The Fitbit user's identifier
        :type user_id: String
        """
        self._fitbit.subscription(user_id, '2')  # TODO: make subscriptionId a config

    def get_authorize_url(self):
        """
        Gets a url to which authorizations request can be sent

        :return: Fitbit authorization url
        :rtype: String
        """
        url, _ = self._fitbit.client.authorize_token_url()
        return url

    def get_activities(self, user_id, date):
        url = "{0}/{1}/user/{2}/activities/date/{date}.json".format(
            *self._fitbit._get_common_args(user_id),
            date=self._fitbit._get_date_string(date)
        )
        return self._fitbit.make_request(url)

    def get_sleep(self, user_id, date):
        url = "{0}/1.2/user/{1}/sleep/date/{date}.json".format(
            self._fitbit.API_ENDPOINT,
            user_id,
            date=self._fitbit._get_date_string(date)
        )
        return self._fitbit.make_request(url)

    def get_bmi(self, user_id, date):
        return self._fitbit.time_series('body/bmi', user_id=user_id, end_date=date)

    def get_body_fat_percent(self, user_id, date):
        return self._fitbit.time_series('body/fat', user_id=user_id, end_date=date)

    def get_weight(self, user_id, date):
        return self._fitbit.time_series('body/weight', user_id=user_id, end_date=date)

    def _update_token(self, token):
        user_token = FitbitToken.query.filter_by(user_id=token['user_id']).first()
        if user_token is None:
            user_token = FitbitToken()
            db.session.add(user_token)

        for key in token.keys():
            setattr(user_token, key, token[key])

        db.session.commit()
