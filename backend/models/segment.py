from backend.database import db


class Segment(db.Model):
    __tablename__ = 'segment'
    segment_id = db.Column(db.Integer, primary_key=True)
    offset = db.Column(db.Numeric(4, 4), nullable=False)
    info = db.Column(db.Text, nullable=False, default='')
    report_id = db.Column(db.Integer, db.ForeignKey('report.report_id', ondelete='CASCADE'), nullable=False)
