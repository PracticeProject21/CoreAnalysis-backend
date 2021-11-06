from flask import Blueprint

auth = Blueprint('core_api', __name__)


@auth.route('/login/')
def login():
    pass
