from glycemiq_server import create_app
from glycemiq_server.models import *

db.create_all(app=create_app())