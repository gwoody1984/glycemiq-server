from flask import Flask

from .config import config_as_dict


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_as_dict('FLASK'))

    from .fitbit import fitbit as fitbit_blueprint
    app.register_blueprint(fitbit_blueprint, url_prefix='/fitbit')

    return app
