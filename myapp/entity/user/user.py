from myapp import db


class User(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    nickname = db.Column(db.String(30))
