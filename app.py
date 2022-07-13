from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import getURI
from controller import routeApi

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = getURI()
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
from entity import User, Photo
db.create_all()


routeApi(app)

if __name__ == '__main__':
    app.run()

