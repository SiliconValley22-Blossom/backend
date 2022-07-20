from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, create_refresh_token,
get_jwt_identity, unset_jwt_cookies
)
from flask_restx import Api as DocApi
from flask_restful import Resource, Api, fields, marshal_with

# import Config

db = SQLAlchemy()
migrate = Migrate()
jwt_redis = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)


def create_app():
    app = Flask(__name__)
    doc_api = DocApi(app, version="1.0",title='Blossom API Server', description='설명', doc='/api-docs')

    from .configs import getURI
    from .controller import routeApi
    app.config['SQLALCHEMY_DATABASE_URI'] = getURI()
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # app.config['JWT_SECRET_KEY'] = Config.key
    # app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.access
    # app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.refresh

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)
    from .entity import User, Photo
    # db.create_all()

    routeApi(doc_api)
    from .controller.PhotoController import nsPhoto
    from .controller.UserController import nsUser
    from .controller.RefreshController import nsRefresh
    from .controller.LoginController import nsLogin
    from .controller.LogoutController import nsLogout
    from .controller.AccessController import nsAccess
    doc_api.add_namespace(nsPhoto)
    doc_api.add_namespace(nsUser)
    doc_api.add_namespace(nsRefresh)
    doc_api.add_namespace(nsLogin)
    doc_api.add_namespace(nsAccess)
    doc_api.add_namespace(nsAdmin)
    doc_api.add_namespace(nsLogout)


    return app