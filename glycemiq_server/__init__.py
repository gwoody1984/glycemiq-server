import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from thespian.actors import ActorSystem

from .config import config_as_obj


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_as_obj('FLASK'))
    db.init_app(app)

    from .fitbit import fitbit as fitbit_blueprint
    app.register_blueprint(fitbit_blueprint, url_prefix='/fitbit')

    return app


def create_actor_sys():
    return ActorSystem('multiprocTCPBase')