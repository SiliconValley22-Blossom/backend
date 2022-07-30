from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request
from flask_restx import Namespace, Resource

from myapp.service.LoginService import LoginService

nsLogout = Namespace('api/logout')


@nsLogout.route("")
class LogoutController(Resource):
    def post(self):
        '''회원 로그아웃'''
        if verify_jwt_in_request(locations=['cookies'], optional=True):
            loginService = LoginService()
            refresh_token = request.cookies['refresh_token_cookie']
            resp = loginService.logout(refresh_token)
        else:
            resp = jsonify({'message':'로그아웃 되었습니다.'})
        # 쿠키 삭제
        resp.set_cookie('access_token_cookie', '', expires=0)
        resp.set_cookie('refresh_token_cookie', '', expires=0)
        return resp