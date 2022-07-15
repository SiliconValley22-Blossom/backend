from sqlalchemy.orm import backref

from myapp import db


class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    nickname = db.Column(db.String(30))

    # photo = db.relationship('Photo', backref=backref('photo_set'))

    check_deleted = db.Column(db.Boolean)

class Photo(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    photo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    fileFormat = db.Column(db.String(10))
    user = db.Column(db.Integer)
    # , db.ForeignKey('user.user_id'))
    is_deleted = db.Column(db.Boolean, default=False)
