from backend.core_api.fields_control import go_next_level, config, EndOfTree, InvalidFormat
import json
from backend.models.segment import Segment
from backend.models.user import User
from backend.models.report import Report

from backend.database import db
from typing import Dict, List, AnyStr

from backend.core_api.fields_control import config, delete_mentioned_property


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


def find_property(source, props):
    """Поиск следующего свойства"""
    for field in source:
        try:
            next(x for x in props.keys() if x == field['name'])
        except StopIteration:
            continue
        else:
            return field
    return None


def find_value(vals, val_name):
    try:
        found_val = next(x for x in vals if x['name'] == val_name)
    except StopIteration:
        return None
    return found_val


def convert_segment_to_readable_view(segment: Segment) -> List[Dict]:
    info = json.loads(segment.info)
    source = config
    out_list = list()
    next_sources = []
    while True:
        prop = find_property(source, info)
        if prop:
            val = find_value(prop['values'], info[prop['name']])
            if val:
                out_list.append({'name': prop['name'], 'title': prop['title'], "value": {
                    'name': val['name'],
                    'title': val['title']
                }})
                del info[prop['name']]
                try:
                    next_sources.append(val['nested'])
                except KeyError:
                    pass
            else:
                del info[prop['name']]

        else:
            try:
                source = next_sources.pop(0)
            except IndexError:
                break
    return out_list


