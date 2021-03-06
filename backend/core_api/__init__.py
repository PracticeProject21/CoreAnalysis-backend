from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from .fields_control import get_properties
from .save_photo import save_photo

from backend.database import db
import io
from PIL import Image

from backend.report_api.report_func import convert_report_to_json
from backend.CoreAnalysis_ML.ML_core.main import ML_part
#
# from backend.models.report import Report
# from backend.models.segment import Segment

from .generate_report import gen_report, convert_segment_info_to_report

api = Blueprint('core_api', __name__)


@api.route('/report/', methods=['POST', "GET"])
@login_required
def get_report():
    photo_type = request.values.get('type')
    photo_name = request.values.get('photo_name', 'Nodata')
    if photo_type not in ('sun', 'ultraviolet'):
        return {
            "message": "type must be 'sun' or 'ultraviolet'"
        }, 400

    if not request.data:
        return {
            "message": "file is required"
        }, 400
    photo_url = save_photo(request.data)
    # report = gen_report(current_user.user_id, photo_type, photo_url, photo_name)
    segments = ML_part(Image.open(io.BytesIO(request.data)), photo_type)
    report = convert_segment_info_to_report(photo_type, segments, photo_name=photo_name, photo_url=photo_url)
    db.session.add(report)
    db.session.commit()
    return convert_report_to_json(report)


@api.route('/fields/', methods=['GET'])
@login_required
def get_fields():
    params = request.args
    return jsonify(get_properties(params))
