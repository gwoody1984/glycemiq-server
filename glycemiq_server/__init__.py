from flask import Flask
from glycemiq_db import db
from thespian.actors import ActorSystem

from glycemiq_server.config import config_as_obj


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_as_obj('FLASK'))
    db.init_app(app)

    from .fitbit import fitbit as fitbit_blueprint
    app.register_blueprint(fitbit_blueprint, url_prefix='/fitbit')
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


def create_actor_sys():
    return ActorSystem('multiprocTCPBase')
