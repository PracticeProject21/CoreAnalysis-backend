import os

from flask import Flask
from flask_login import LoginManager

from backend.core_api import api
from backend.auth.route import auth
from flask_cors import CORS
from .database import db
from .models.user import User


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')

    @app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE'
        return response

    app.register_blueprint(api, url_prefix='/api/')
    app.register_blueprint(auth, url_prefix='/users/')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    return app
