from flask_restful import reqparse
from myapp.entity.Entity import User
from myapp.service import LoginService
from flask_restx import Namespace, Resource, fields

nsLogin = Namespace('api/login')

login = nsLogin.model('Login',{
    "email":fields.String(required=True),
    "password":fields.String(required=True)
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

    def get(self):
        # 로직
        result = 'group'
        return result, 200

    @nsLogin.expect(login)
    def post(self):
        data = LoginController.requestParser.parse_args()
        # try:
        loginRequest = LoginRequest(data)
        loginService = LoginService.LoginService()
        result = loginService.login(loginRequest)
        return LoginResponse(result).__dict__
