from flask_restful import Api
from myapp.controller import *


def routeApi(app):
    api = Api(app)
    api.add_resource(UserController, '/users')
    api.add_resource(PhotoController, '/photos')