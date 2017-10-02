from glycemiq_server import create_app
from glycemiq_db import *

db.create_all(app=create_app())
