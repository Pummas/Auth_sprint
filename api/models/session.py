from sqlalchemy import ForeignKey

from core.config import db


class Session(db.Model):
    __tablename__ = 'session'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
    login_time = db.Column(db.DateTime)
