from flask_restful import Api
from .PhotoController import *
from .UserController import *

def routeApi(app):
    api = Api(app)
    api.add_resource(UserController, '/api/users')
    api.add_resource(UserSingleController, '/api/users/<int:user_id>')
    api.add_resource(PhotoController, '/api/photos')
    api.add_resource(ColorizedPhoto, '/api/photos/<int:photoId>')