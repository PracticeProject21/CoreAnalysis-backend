from backend.database import db

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(db.Integer, primary_key=True)
    json_date = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_id'), nullable=False)
    reports = db.relationship('Segment', backref='segment')
