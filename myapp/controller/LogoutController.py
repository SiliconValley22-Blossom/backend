from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required, set_access_cookies, set_refresh_cookies, \
    verify_jwt_in_request
from flask_restx import Namespace, Resource

from myapp.service.LoginService import LoginService

nsLogout = Namespace('api/logout')


@nsLogout.route("")
class LogoutController(Resource):
    def post(self):
        if verify_jwt_in_request(locations=['cookies'], optional=True):
            loginService = LoginService()
            resp = loginService.logout()
        else:
            resp = jsonify({'message':'로그아웃 되었습니다.'})
        # 쿠키 삭제
        resp.set_cookie('access_token_cookie', '', expires=0)
        resp.set_cookie('refresh_token_cookie', '', expires=0)
        return resp