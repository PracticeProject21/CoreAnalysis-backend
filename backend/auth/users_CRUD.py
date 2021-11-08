from flask import request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from . import auth
from backend.database import db
from backend.models.user import User


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


@auth.route('/<int:user_id>/', methods=['PATCH'])
@login_required
def patch_info_by_id(user_id):
    User.query.get_or_404(user_id)

    if request.json is None:
        return {
                   "message": "Empty body"
               }, 400

    name = request.json.get('name')
    password = request.json.get('password')
    is_admin = request.json.get('is_admin')
    if is_admin is not None:
        is_admin = is_admin == 'true'

    props = {}
    if name is not None:
        props['name'] = name
    if password is not None:
        props['password'] = generate_password_hash(password, method='sha256')
    if is_admin is not None:
        props['is_admin'] = is_admin

    if props:
        db.session.query(User).filter_by(user_id=user_id).update(props)
    db.session.commit()

    return '', 204


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
