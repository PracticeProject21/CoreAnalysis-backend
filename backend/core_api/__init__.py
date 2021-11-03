from flask import Blueprint, request, jsonify

from .fields_control import get_properties

api = Blueprint('core_api', __name__)


@api.route('/report/', methods=['POST'])
def get_report():
    photo_type = request.values.get('type')
    if photo_type not in ('sun', 'ultraviolet'):
        return {
            "message": "type must be 'sun' or 'ultraviolet'"
        }, 400
    file = request.files['file']
    if not file:
        return {
            "message": "file is required"
        }, 400
    return {
        "report_id": 1,
        "photo": "https://i.picsum.photos/id/1031/200/3000.jpg?hmac=c28LIVtJE8EpnqWXFYrnfeS-nPWafthF-XkQN4DHHg8",
        "photo_type": photo_type,
        "segments":
            [
                {
                    "segment_id": 1,
                    "percent": 0.36,
                    "properties":
                        [
                            {
                                "name": "sun_type",
                                "title": "Тип",
                                "value":
                                    {
                                        "name": "formation",
                                        "title": "Порода"
                                    }
                            },
                            {
                                "name": "formation_type",
                                "title": "Тип",
                                "value":
                                    {
                                        "name": "sandstone",
                                        "title": "Песчанник"
                                    }
                            }

                        ]
                },
                {
                    "segment_id": 2,
                    "percent": 0.64,
                    "properties":
                        [
                            {
                                "name": "sun_type",
                                "title": "Тип",
                                "value":
                                    {
                                        "name": "destruction",
                                        "title": "Разрушенность"
                                    }
                            },
                            {
                                "name": "destruction_type",
                                "title": "Тип",
                                "value":
                                    {
                                        "name": "fault",
                                        "title": "Разлом"
                                    }
                            }

                        ]
                }
            ]
    }


@api.route('/fields/', methods=['GET'])
def get_fields():
    params = request.args
    return jsonify(get_properties(params))
