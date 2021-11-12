from backend.database import db
from .field import Field


class Segment(db.Model):
    __tablename__ = 'segment'
    segment_id = db.Column(db.Integer, primary_key=True)
    segment_type = db.Column(db.String(30), nullable=False)
    fields = db.relationship(Field)
    report_id = db.Column(db.Integer, db.ForeignKey('report.report_id', ondelete='CASCADE'), nullable=False)
