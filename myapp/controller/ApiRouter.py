from flask_restful import Api
from myapp.controller import *


def routeApi(app):
    api = Api(app)
    api.add_resource(UserController, '/users', '/users/<int:user_id>')
    api.add_resource(PhotoController, '/photos')
    api.add_resource(ColorizedPhoto, '/photos/<int:photo_id>')