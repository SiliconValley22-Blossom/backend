from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Medel):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30))
    password = db.Column(db.String(30))
    nickname = db.Column(db.String(30))
