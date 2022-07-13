from flask import Flask

from config import setInitMigrate
from controller import routeApi


def create_app():
    app = Flask(__name__)
    routeApi(app)
    setInitMigrate(app)
    return app


"""
def create_app():
    app = Flask(__name__)
    api = Api(app)
    db = SQLAlchemy(app)

    api.add_resource(UserController, '/users')
    api.add_resource(PhotoController, '/photos/')
    api.add_resource(ColorizedPhoto, '/photos/<id>')

    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123qwe@localhost:3306/test_blossom"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    return app
    
"""