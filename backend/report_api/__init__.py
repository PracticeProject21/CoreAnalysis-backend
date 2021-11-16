from flask import Blueprint, jsonify, request
import json

from backend.models.report import Report
from .report_func import convert_report_to_json
from backend.database import db
from ..models.segment import Segment

report = Blueprint('report_api', __name__)


@report.route('/reports/', methods=['GET'])
def get_all_reports():
    rep = Report.query.all()
    answer = []
    for r in rep:
        answer.append(convert_report_to_json(r))
    return jsonify(answer)


@report.route('/reports/<int:report_id>/', methods=['GET'])
def get_reports(report_id):
    rep = Report.query.get_or_404(report_id)
    return convert_report_to_json(rep)


@report.route('/reports/<int:report_id>/', methods=['DELETE'])
def get_reports_by_id(report_id):
    db.session.query(Report).filter_by(report_id=report_id).delete()
    db.session.commit()


@report.route('/segments/<int:segment_id>/', methods=['PUT', "PATCH"])
def update_segment(segment_id):
    Segment.query.get_or_404(segment_id)
    props = {}
    data = json.loads(request.data.decode())
    if data.get('offset'):
        props['offset'] = data.get('offset')
    if data.get('properties'):
        props['info'] = json.dumps(data.get('properties'))
    print(props)

    db.session.query(Segment).filter_by(segment_id=segment_id).update(props)
    db.session.commit()
    return '', 204


@report.route('/segments/<int:segment_id>/', methods=['DELETE'])
def delete_segment(segment_id):
    Segment.query.get_or_404(segment_id)
    db.session.query(Segment).filter_by(segment_id=segment_id).delete()
    db.session.commit()
    return '', 204

