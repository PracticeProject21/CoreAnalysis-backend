import os

from flask import Flask
from flask_login import LoginManager

from backend.core_api import api
from backend.auth.route import auth
from flask_cors import CORS
from .database import db
from .models.user import User
from .models.report import Report
from .models.segment import Segment


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    db.init_app(app)
    database = os.environ.get('DATABASE_URL')
    if 'DYNO' in os.environ:
        database = database.replace("://", "ql://", 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database

    @app.after_request
    def apply_caching(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response.headers['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS, PUT, DELETE, PATCH'
        return response

    app.register_blueprint(api, url_prefix='/api/')
    app.register_blueprint(auth, url_prefix='/users/')

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.request_loader
    def load_user_from_request(request):
        auth_header = request.headers.get('Authorization')
        user_id = User.decode_auth_token(auth_header)
        if isinstance(user_id, str):
            return None
        user = User.query.get_or_404(user_id)
        return user

    with app.app_context():
        db.create_all()  # Create sql tables for our data models

    return app
