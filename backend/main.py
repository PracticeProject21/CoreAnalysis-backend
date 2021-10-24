import os

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    @app.route('/')
    def hello():
        return {'hello': 'world'}

    return app