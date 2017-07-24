#! /usr/bin/env python

import os

from glycemiq_server import create_app

from flask_script import Manager

app = create_app(os.getenv('GLYCEMIQ_ENV') or 'dev')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
