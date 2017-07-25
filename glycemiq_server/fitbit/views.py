import sys
import traceback

from flask import redirect, request
from oauthlib.oauth2 import MismatchingStateError, MissingTokenError

from . import fitbit
from .OAuth2Server import OAuth2Server
from ..config import config_as_dict


config = config_as_dict('FITBIT')
server = OAuth2Server(config['CLIENT_ID'], config['CLIENT_SECRET'], config['AUTH_CALLBACK_URL'])


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
    if code:
        try:
            token = server.fitbit.client.fetch_access_token(code)
        except MissingTokenError:
            error = _fmt_failure(
                'Missing access token parameter.</br>Please check that '
                'you are using the correct client_secret')
        except MismatchingStateError:
            error = _fmt_failure('CSRF Warning! Mismatching state')
    else:
        error = _fmt_failure('Unknown error while authenticating')

    return error if error else server.success_html


def _fmt_failure(message):
    tb = traceback.format_tb(sys.exc_info()[2])
    tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
    return server.failure_html % (message, tb_html)