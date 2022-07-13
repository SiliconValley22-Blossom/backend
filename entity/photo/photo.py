from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Photo(db.Model):
    photo_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    fileFormat = db.Column(db.String(10))
    user = db.Column(db.Integer)
    #, db.ForeignKey('user.user_id')
