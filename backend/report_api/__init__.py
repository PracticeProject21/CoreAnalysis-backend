import os

from flask import Blueprint, jsonify, request, send_from_directory
from flask_login import login_required, current_user
import json

from backend.models.report import Report
from backend.report_api.generate_report_file import generate_file
from .report_func import convert_report_to_json, convert_segments_to_json
from backend.database import db
from ..models.segment import Segment

report = Blueprint('report_api', __name__)


@report.route('/reports/', methods=['GET'])
@login_required
def get_all_reports():
    rep = Report.query.all()
    answer = []
    for r in rep:
        answer.append(convert_report_to_json(r))
    return jsonify(answer)


@report.route('/reports/<int:report_id>/', methods=['GET'])
@login_required
def get_reports(report_id):
    rep = Report.query.get_or_404(report_id)
    return convert_report_to_json(rep)


@report.route('/reports/<int:report_id>/file/', methods=['GET'])
@login_required
def get_report_file(report_id):
    rep = Report.query.get_or_404(report_id)
    filename = generate_file(convert_report_to_json(rep))
    return send_from_directory(os.getcwd(), filename)


@report.route('/reports/<int:report_id>/', methods=['DELETE'])
@login_required
def get_reports_file_by_id(report_id):
    db.session.query(Report).filter_by(report_id=report_id).delete()
    db.session.commit()


@report.route('/segments/<int:segment_id>/', methods=['PUT', "PATCH"])
@login_required
def update_segment(segment_id):
    Segment.query.get_or_404(segment_id)
    props = {}
    data = json.loads(request.data.decode())
    props['offset'] = data.get('offset') or 0
    props['info'] = json.dumps(data.get('properties') or {})
    print(props)

    db.session.query(Segment).filter_by(segment_id=segment_id).update(props)
    db.session.commit()
    return '', 204


@report.route('/segments/<int:segment_id>/', methods=['DELETE'])
@login_required
def delete_segment(segment_id):
    Segment.query.get_or_404(segment_id)
    db.session.query(Segment).filter_by(segment_id=segment_id).delete()
    db.session.commit()
    return '', 204


@report.route('/reports/<int:report_id>/add_segment/', methods=['POST'])
@login_required
def create_segment(report_id):
    cur_report = Report.query.get_or_404(report_id)
    segment = Segment(offset=0.9999, info="{}", report_id=cur_report.report_id)
    db.session.add(segment)
    db.session.commit()
    return convert_segments_to_json([segment])[0], 201
