from backend.database import db


class Segment(db.Model):
    __tablename__ = 'segment'
    segment_id = db.Column(db.Integer, primary_key=True)
    segment_type = db.Column(db.String(30), nullable=False)
    info = db.Column(db.String(255), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report_id'), nullable=False)
