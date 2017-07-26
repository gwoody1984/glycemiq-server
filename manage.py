#! /usr/bin/env python

from glycemiq_server import create_app

app = create_app()

@app.route('/')
def index():
    return 'Glycemiq API'


if __name__ == '__main__':
    app.run()
