from flask_restful import Resource, reqparse
from myapp.entity.Entity import User
from myapp.service import LoginService

class LoginRequest:
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']


class LoginController(Resource):
    # Request Fields
    saveRequest = reqparse.RequestParser()
    saveRequest.add_argument('email', type=str, nullable=False, trim=True)
    saveRequest.add_argument('password', type=str, nullable=False, trim=True)


    def get(self):
        # 로직
        result = 'group'
        return result, 200

    def post(self):
        data = LoginController.saveRequest.parse_args()
        try:
            loginRequest = LoginRequest(data)
            loginService = LoginService.LoginService()
            result = loginService.login(loginRequest)
            return result
        except Exception as e:
            print(str(e))
            return str(e), 400

