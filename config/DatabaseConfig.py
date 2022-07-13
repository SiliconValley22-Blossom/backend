from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

DB_USERNAME = 'root'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_SCHEMA = 'blossom'
DB_PORT = '3306'

SQLALCHEMY_TRACK_MODIFICATIONS = False

def getURI():
    return f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}'

def setInitMigrate(app):
    db = SQLAlchemy(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    migrate.init_app(app, db)
