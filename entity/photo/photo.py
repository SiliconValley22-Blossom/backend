from flask_sqlalchemy import SQLAlchemy
from app import db


class Photo(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    photo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    fileFormat = db.Column(db.String(10))
    user = db.Column(db.Integer)
    # , db.ForeignKey('user.user_id')
