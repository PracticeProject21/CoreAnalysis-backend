from backend.database import db


class Field(db.Model):
    __tablename__ = 'fields'
    field_id = db.Column(db.Integer, primary_key=True)
    field_type = db.Column(db.String(30), nullable=False)
    field_value = db.Column(db.String(30), nullable=False)
    segment_id = db.Column(db.Integer, db.ForeignKey('segment.segment_id', ondelete='CASCADE'), nullable=False)
