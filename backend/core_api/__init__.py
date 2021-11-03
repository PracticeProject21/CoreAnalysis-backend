from flask import Blueprint, request, jsonify

from .fields_control import get_properties

api = Blueprint('core_api', __name__)


@api.route('/report/', methods=['POST'])
def get_report():
    file = request.files['file']
    return {
        "filename": file.filename
    }


@api.route('/fields/', methods=['GET'])
def get_fields():
    params = request.args
    return jsonify(get_properties(params))
