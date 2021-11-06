from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from backend.database import db
from backend.models.user import User

auth = Blueprint('auth', __name__)


def admin_required(fun):
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            return fun(*args, **kwargs)
        else:
            return {'message': "Access denied"}, 403

    return wrapper


@auth.route('/my/', methods=['GET'])
@login_required
def get_info():
    return {
        'user_id': current_user.user_id,
        'name': current_user.name,
        'is_admin': current_user.is_admin
    }


@auth.route('/', methods=['GET'])
@login_required
def get_all_users_info():
    users = User.query
    if request.values.get('name'):
        users = users.filter(User.name.like(request.values.get('name') + '%'))
    if request.values.get('is_admin'):
        users = users.filter_by(is_admin=bool(request.values.get('is_admin') == 'true'))
    out = []
    for user in users.all():
        out.append(
            {
                "user_id": user.user_id,
                'name': user.name,
                'is_admin': user.is_admin
            })
    return jsonify(out)


@auth.route('/<int:user_id>/', methods=['GET'])
@login_required
def get_info_by_id(user_id):
    user = User.query.get_or_404(user_id)
    return {
                "user_id": user.user_id,
                'name': user.name,
                'is_admin': user.is_admin
            }


@auth.route('/', methods=['POST'])
@admin_required
def create_user():
    name = request.json.get('name')
    password = request.json.get('password')
    is_shop = request.json.get('is_admin', '').lower() == 'true'

    if name is None:
        return 'Name is required', 422
    if password is None:
        return 'Password is required', 422

    user = User.query.filter_by(name=name).first()
    if user:
        return 'User already exist', 409

    new_user = User(name=name,
                    is_admin=is_shop,
                    password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    return '', 201


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
