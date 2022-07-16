from flask_restful import Resource, reqparse
from myapp.entity.Entity import User
from myapp.service import UserService

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