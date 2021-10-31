import os

from flask import Flask

from backend.core_api import api
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    @app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
        return response

    app.register_blueprint(api, url_prefix='/api/')

    return app
