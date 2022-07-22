
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import redis

from flask_jwt_extended import (
    JWTManager
)
from flask_migrate import Migrate
from flask_restx import Api as DocApi
from flask_sqlalchemy import SQLAlchemy

# import Config
from prometheus_flask_exporter import PrometheusMetrics
import datetime

import redis

db = SQLAlchemy()
migrate = Migrate()
jwt_redis = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)



def create_app():
    app = Flask(__name__)
    doc_api = DocApi(app, version="1.0",title='Blossom API Server', description='설명', doc='/api/docs')

    from .configs import getURI
    from .controller import routeApi
    app.config['SQLALCHEMY_DATABASE_URI'] = getURI()
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = "secret123!@#"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(days=14)
    metrics = PrometheusMetrics(app)

    metrics.register_default(
        metrics.counter(
            'by_path_counter', 'Request count by request paths',
            labels={'path': lambda: request.path}
        )
    )

    jwt = JWTManager(app)

    # db.init_app(app)
    # migrate.init_app(app, db)
    app.app_context().push()
    db.init_app(app)
    migrate = Migrate(app, db)
    # flask-migrate 적용
    db.create_all()


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
    # doc_api.add_namespace(nsAdmin)
    doc_api.add_namespace(nsLogout)
    CORS(app, supports_credentials=True)


    return app
