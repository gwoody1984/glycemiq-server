from flask import Flask
from thespian.actors import ActorSystem

from .config import config_as_dict

actor_sys = ActorSystem('multiprocTCPBase')

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_as_dict('FLASK'))

    from .fitbit import fitbit as fitbit_blueprint
    app.register_blueprint(fitbit_blueprint, url_prefix='/fitbit')

    return app
