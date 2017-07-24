from flask import Blueprint

fitbit = Blueprint('fitbit', __name__)

from . import views