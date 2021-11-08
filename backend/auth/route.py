from flask import request
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash

from backend.models.user import User
from . import auth
from .users_CRUD import *


@auth.route('/login/', methods=["GET"])
def login():
    password = request.values.get('password')
    name = request.values.get('name')

    if password is None or name is None:
        return 'Name and password is requires', 422

    user = User.query.filter_by(name=name).first_or_404()
    if not check_password_hash(user.password, password):
        return 'Password is invalid', 400

    token = user.encode_auth_token(user.user_id)
    return {'token': token}, 200
