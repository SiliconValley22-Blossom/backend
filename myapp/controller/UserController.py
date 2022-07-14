from flask_restful import Resource, reqparse

from myapp.service import UserService


class UserRequest:
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        self.nickname = data['nickname']


class UserController(Resource):
    # Request Fields
    saveRequest = reqparse.RequestParser()
    saveRequest.add_argument('email', type=str, nullable=False, trim=True)
    saveRequest.add_argument('nickname', type=str, nullable=False, trim=True)
    saveRequest.add_argument('password', type=str, nullable=False, trim=True)

    def get(self):
        # 로직
        result = 'group'
        return result, 200

    def post(self):
        data = UserController.saveRequest.parse_args()
        userRequest = UserRequest(data)
        userService = UserService()
        result = userService.save(userRequest)
        return 'result', 201

    def delete(self):
        # 로직
        result = None
        return result, 204