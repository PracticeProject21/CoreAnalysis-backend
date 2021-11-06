from flask_login import UserMixin

from backend.database import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    reports = db.relationship('Report', backref='report')

    def get_id(self):
        return self.user_id
