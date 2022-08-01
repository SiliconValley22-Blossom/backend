import datetime
import os

import redis
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager
)
from flask_mail import Mail
from flask_migrate import Migrate
from flask_restx import Api as DocApi
from flask_sqlalchemy import SQLAlchemy
from prometheus_flask_exporter import PrometheusMetrics

from .configs import JWT_KEY, JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_TOKEN_EXPIRES

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
jwtRedis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)

metrics = PrometheusMetrics.for_app_factory()
#metrics = GunicornInternalPrometheusMetrics.for_app_factory()


def create_app():
    app = Flask(__name__)
    doc_api = DocApi(app, version="2.0", title='Blossom API Server', description='Blossom Backend API Documentation', doc='/api/docs')

    from .configs import getURI
    app.config['SQLALCHEMY_DATABASE_URI'] = getURI()
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = JWT_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = JWT_ACCESS_TOKEN_EXPIRES
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = JWT_REFRESH_TOKEN_EXPIRES

    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

    metrics.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    jwt = JWTManager(app)

    app.app_context().push()

    from myapp.controller import routeApi
    routeApi(doc_api)
    from .controller.PhotoController import nsPhoto
    from .controller.UserController import nsUser
    from .controller.RefreshController import nsRefresh
    from .controller.LoginController import nsLogin
    from .controller.LogoutController import nsLogout
    from .controller.AdminController import nsAdmin
    doc_api.add_namespace(nsPhoto)
    doc_api.add_namespace(nsUser)
    doc_api.add_namespace(nsRefresh)
    doc_api.add_namespace(nsLogin)
    doc_api.add_namespace(nsAdmin)
    doc_api.add_namespace(nsLogout)
    CORS(app, supports_credentials=True)

    return app
