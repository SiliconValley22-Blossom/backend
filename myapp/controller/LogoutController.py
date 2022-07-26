from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies
from flask_restx import Namespace, Resource

from myapp.service.LoginService import LoginService

nsLogout = Namespace('api/logout')


@nsLogout.route("")
class LogoutController(Resource):
    @jwt_required(locations=['cookies'])
    def get(self):
        loginService = LoginService()
        resp = loginService.logout()
        return resp
