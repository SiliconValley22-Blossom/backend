from dataclasses import dataclass
from datetime import datetime

from sqlalchemy.orm import backref

from myapp import db


@dataclass
class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    user_id: int
    email: str
    nickname: str
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(35), nullable=False)
    nickname = db.Column(db.String(30), nullable=False)
    user_role = db.Column(db.String(10), nullable=False, default='guest')
    photo = db.relationship('Photo', backref=backref('photo'))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=0)


class Photo(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    photo_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'))
    name = db.Column(db.String(30))
    file_format = db.Column(db.String(10))
    url = db.Column(db.String(100))
    color_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id', ondelete='CASCADE'), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
