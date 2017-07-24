from flask import Flask

from .config import config_section


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_section('FLASK'))

    from .fitbit import fitbit as fitbit_blueprint
    app.register_blueprint(fitbit_blueprint, url_prefix='/fitbit')

    return app
