from flask import Flask

from .config import config_by_env


def create_app(environment):
    app = Flask(__name__)
    app.config.from_object(config_by_env[environment])

    from .fitbit import fitbit as fitbit_blueprint
    app.register_blueprint(fitbit_blueprint, url_prefix='/fitbit')

    return app
