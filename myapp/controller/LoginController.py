from flask import jsonify
from flask_jwt_extended import set_access_cookies, set_refresh_cookies, verify_jwt_in_request
from flask_restful import reqparse
from flask_restx import Namespace, Resource, fields

from myapp.service import LoginService

nsLogin = Namespace('api/login')

login = nsLogin.model('LoginForm', {
    "email": fields.String(required=True),
    "password": fields.String(required=True)
})


class LoginRequest:
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']


class LoginResponse:
    def __init__(self, data):
        self.Authorization = data


@nsLogin.route('')
class LoginController(Resource):
    # Request Fields
    requestParser = reqparse.RequestParser()
    requestParser.add_argument('email', type=str, nullable=False, trim=True)
    requestParser.add_argument('password', type=str, nullable=False, trim=True)

    @nsLogin.expect(login)
    @nsLogin.response(200, "Login Successfully")
    def post(self):
        '''회원 로그인'''
        data = LoginController.requestParser.parse_args()
        loginRequest = LoginRequest(data)
        loginService = LoginService.LoginService()
        access, refresh = loginService.login(loginRequest)

        resp = jsonify({'message': 'Login Successfully'})
        set_access_cookies(resp, access)
        set_refresh_cookies(resp, refresh)
        return resp


@nsLogin.route('/check')
class CheckLoginController(Resource):
    @nsLogin.response(200, "로그인 되어 있을 때", nsLogin.model('Checklogin', {'is_login': fields.Boolean}))
    @nsLogin.response(401, "로그인 안 되어 있을 때", nsLogin.model('Checklogin', {'is_login': fields.Boolean}))
    def get(self):
        '''회원 로그인 여부 확인'''
        if verify_jwt_in_request(locations=['cookies'], optional=True):
            resp = jsonify({'is_login': True})
        else:
            resp = jsonify({'is_login': False})
        return resp
