from flask import Blueprint, request

api = Blueprint('core_api', __name__)


@api.route('/report/', methods=['POST'])
def get_report():
    file = request.files['file']
    return {
        "filename": file.filename
    }
