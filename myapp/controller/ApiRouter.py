from .AdminController import AdminUserController
from .LogoutController import LogoutController
from .PhotoController import *
from .RefreshController import RefreshController
from .UserController import *
from .LoginController import *


def routeApi(api):
    api.add_resource(UserController, '/api/users')
    api.add_resource(UserSingleController, '/api/users/<int:user_id>')
    api.add_resource(UserPwController, '/api/users/reset-pw')
    api.add_resource(PhotoController, '/api/photos')
    api.add_resource(PhotoSingleController, '/api/photos/<int:photo_id>')
    api.add_resource(LoginController, '/api/login')
    api.add_resource(CheckLoginController, '/api/login/check')
    api.add_resource(LogoutController, '/api/logout')
    api.add_resource(RefreshController, '/api/refresh')
    api.add_resource(AdminUserController, '/api/admin/users')



from werkzeug.wrappers import Request
from werkzeug.wsgi import responder
from werkzeug.exceptions import HTTPException, NotFound


def view(request):
    raise NotFound()


@responder
def application(environ, start_response):
    request = Request(environ)
    try:
        return view(request)
    except HTTPException as e:
        return e