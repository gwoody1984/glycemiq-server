#! /usr/bin/env python

import os

from glycemiq_server import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
