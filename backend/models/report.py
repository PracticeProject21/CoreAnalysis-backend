from backend.database import db


class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True)
    photo_type = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    segments = db.relationship('Segment', backref='report')
