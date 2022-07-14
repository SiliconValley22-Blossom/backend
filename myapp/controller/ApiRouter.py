from flask_restful import Api
from .PhotoController import *
from .UserController import *

def routeApi(app):
    api = Api(app)
    api.add_resource(UserController, '/users')
    api.add_resource(UserSingleController, '/users/<int:user_id>')
    api.add_resource(PhotoController, '/photos')
    api.add_resource(ColorizedPhoto, '/photos/<int:photo_id>')