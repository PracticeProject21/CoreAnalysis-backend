from backend.core_api.fields_control import go_next_level, config, EndOfTree, InvalidFormat
import json
from backend.models.segment import Segment
from backend.models.user import User
from backend.models.report import Report

from backend.database import db
from typing import Dict, List, AnyStr


def validate_segment(json: dict) -> dict:
    """- Delete invalid fields """
    pass


def create_segment(fields: Dict) -> Segment:
    json_data = json.dumps(fields)
    segment = Segment(info=json_data)
    return segment


def create_report(photo_name: AnyStr, photo_url: AnyStr, photo_type: AnyStr, segments: List[Dict],
                  user: User) -> Report:
    report = Report(photo_name=photo_name, photo_url=photo_url, photo_type=photo_type, user_id=user.user_id)
    for segment in segments:
        report.segments.append(create_segment(segment))
    return report
