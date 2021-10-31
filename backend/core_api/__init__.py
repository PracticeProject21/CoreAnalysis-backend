from flask import Blueprint, request

api = Blueprint('core_api', __name__)


@api.route('/report/', methods=['POST'])
def get_report():
    print(request.values.to_dict())
    photo_type = request.values.get('type')
    if photo_type not in ('sun', 'ultraviolet'):
        return {
            "message": "type must be 'sun' or 'ultraviolet'"
        }, 400
    if not request.data:
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
                                "name": "formation_kind",
                                "title": "Вид",
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
                                "name": "destr_kind",
                                "title": "Вид",
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
