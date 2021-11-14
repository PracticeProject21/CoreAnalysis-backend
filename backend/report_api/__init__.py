from flask import Blueprint, jsonify

from backend.models.report import Report
from .report_func import convert_report_to_json
from backend.database import db


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
