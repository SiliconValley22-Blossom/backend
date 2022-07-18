from datetime import datetime

from myapp import db


class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(35), nullable=False)
    nickname = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='guest')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=0)


class Photo(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    photo_id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    name = db.Column(db.String(30))
    fileFormat = db.Column(db.String(10))
    url = db.Column(db.String(100))
    color_id = db.Column(db.Integer, db.ForeignKey('photo.photo_id'), nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_deleted = db.Column(db.Boolean, default=False)
