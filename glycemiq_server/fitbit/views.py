import sys
import traceback

from flask import redirect, request, abort
from oauthlib.oauth2 import MismatchingStateError, MissingTokenError, OAuth2Token

from . import fitbit
from .OAuth2Server import OAuth2Server
from ..config import config_as_dict


config = config_as_dict('FITBIT')
server = OAuth2Server(config['CLIENT_ID'], config['CLIENT_SECRET'], config['AUTH_CALLBACK_URL'])
tokens = {}


@fitbit.route('/auth')
def authorize():
    url = server.browser_authorize()
    return redirect(url)


@fitbit.route('/auth_result')
def authorize_result():
    """
    Receive a Fitbit response containing a verification code. Use the code
    to fetch the access_token.
    """
    code = request.args.get('code')
    state = request.args.get('state')
    error = None
    token_string = ""
    if code:
        try:
            token = server.fitbit.client.fetch_access_token(code)
            _update_token(token)
            token_string = "<p>token: " + token['user_id'] + "</p>"
        except MissingTokenError:
            error = _fmt_failure(
                'Missing access token parameter.</br>Please check that '
                'you are using the correct client_secret')
        except MismatchingStateError:
            error = _fmt_failure('CSRF Warning! Mismatching state')
    else:
        error = _fmt_failure('Unknown error while authenticating')

    return error if error else token_string + server.success_html


@fitbit.route('/subscribe/<string:user_id>')
def subscribe(user_id):
    client_token = tokens.get(user_id)
    server.set_fitbit_client(client_token, _update_token)
    server.fitbit.subscription(user_id, '2')  # MAGIC STRING
    return "Subscription has been set"


@fitbit.route('/notification', methods=['GET'])
def notification_verification():
    verify_code = request.args.get('verify')
    if verify_code == config['SUBSCRIPTION_VERIFICATION_CODE']:
        return ('', 204)
    else:
        abort(404)


@fitbit.route('/notification', methods=['POST'])
def notification():
    return ('', 204)


def _fmt_failure(message):
    tb = traceback.format_tb(sys.exc_info()[2])
    tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
    return server.failure_html % (message, tb_html)


def _update_token(token):
    if token is OAuth2Token:
        tokens.update({token['user_id']: dict(token)})