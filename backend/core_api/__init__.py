from flask import Blueprint, request, jsonify

from .fields_control import get_properties

from backend.database import db

from backend.report_api.report_func import convert_report_to_json

from backend.models.report import Report
from backend.models.segment import Segment

from .generate_report import gen_report

api = Blueprint('core_api', __name__)


@api.route('/report/', methods=['POST', "GET"])
def get_report():
    photo_type = request.values.get('type')
    if photo_type not in ('sun', 'ultraviolet'):
        return {
            "message": "type must be 'sun' or 'ultraviolet'"
        }, 400

    if not request.data:
        return {
            "message": "file is required"
        }, 400
    report = gen_report(1, photo_type)
    db.session.add(report)
    db.session.commit()
    return convert_report_to_json(report)
    # return {
    #     "report_id": 1,
    #     "photo": "https://i.picsum.photos/id/1031/200/3000.jpg?hmac=c28LIVtJE8EpnqWXFYrnfeS-nPWafthF-XkQN4DHHg8",
    #     "photo_type": photo_type,
    #     "segments":
    #         [
    #             {
    #                 "segment_id": 1,
    #                 "percent": 0.36,
    #                 "properties":
    #                     [
    #                         {
    #                             "name": "sun_type",
    #                             "title": "Тип",
    #                             "value":
    #                                 {
    #                                     "name": "formation",
    #                                     "title": "Порода"
    #                                 }
    #                         },
    #                         {
    #                             "name": "formation_kind",
    #                             "title": "Вид",
    #                             "value":
    #                                 {
    #                                     "name": "sandstone",
    #                                     "title": "Песчанник"
    #                                 }
    #                         }
    #
    #                     ]
    #             },
    #             {
    #                 "segment_id": 2,
    #                 "percent": 0.64,
    #                 "properties":
    #                     [
    #                         {
    #                             "name": "sun_type",
    #                             "title": "Тип",
    #                             "value":
    #                                 {
    #                                     "name": "destruction",
    #                                     "title": "Разрушенность"
    #                                 }
    #                         },
    #                         {
    #                             "name": "destr_kind",
    #                             "title": "Вид",
    #                             "value":
    #                                 {
    #                                     "name": "fault",
    #                                     "title": "Разлом"
    #                                 }
    #                         }
    #
    #                     ]
    #             }
    #         ]
    # }


@api.route('/fields/', methods=['GET'])
def get_fields():
    params = request.args
    return jsonify(get_properties(params))
