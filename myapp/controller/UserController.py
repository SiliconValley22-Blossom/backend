import json

from flask import Response
from flask_restful import Resource, reqparse
from myapp.entity.Entity import User
from myapp.service import UserService

class UserRequest:
    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        self.nickname = data['nickname']

class UserResponse:
    def __init__(self, data):
        self.user_id = data.user_id
        self.email = data.email
        self.nickname = data.nickname

class UserController(Resource):
    # Request Fields
    saveParam = reqparse.RequestParser()
    saveParam.add_argument('email', type=str, nullable=False, trim=True)
    saveParam.add_argument('nickname', type=str, nullable=False, trim=True)
    saveParam.add_argument('password', type=str, nullable=False, trim=True)

    def get(self):
        # 로직
        result = 'group'
        return result, 200

    def post(self):

        data = UserController.saveParam.parse_args()

        userRequest = UserRequest(data)
        userService = UserService()
        result = userService.save(userRequest)
        return UserResponse(result).__dict__, 201

class UserSingleController(Resource):
    def get(self, user_id):
        # 로직
        result = user_id
        return result, 200

    def delete(self, user_id):
        userService = UserService()
        userService.deleteById(user_id)

        return Response(status=204)
