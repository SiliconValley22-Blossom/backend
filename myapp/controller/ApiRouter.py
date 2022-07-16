from flask_restful import Api

from .AccessController import AccessController
from .PhotoController import *
from .RefreshController import RefreshController
from .UserController import *
from .LoginController import *

def routeApi(app):
    api = Api(app)
    api.add_resource(UserController, '/api/users')
    api.add_resource(UserSingleController, '/api/users/<int:user_id>')
    api.add_resource(PhotoController, '/api/photos')
    api.add_resource(ColorizedPhoto, '/api/photos/<int:photo_id>')
    api.add_resource(LoginController, '/api/login')
    api.add_resource(AccessController, '/api/access')
    api.add_resource(RefreshController, '/api/refresh')

