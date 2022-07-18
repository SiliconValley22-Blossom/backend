import json

from flask import Response
from flask_restful import reqparse
from myapp.entity.Entity import User
from myapp.service import UserService
from flask_restx import Namespace,fields, Resource

nsUser=Namespace('api/users')
user=nsUser.model('User',{
    'email':fields.String,
    'password':fields.String,
    'nickname':fields.String
})


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


@nsUser.route("")
class UserController(Resource):
    # Request Fields
    requestParser = reqparse.RequestParser()
    requestParser.add_argument('email', type=str, nullable=False, trim=True)
    requestParser.add_argument('nickname', type=str, nullable=False, trim=True)
    requestParser.add_argument('password', type=str, nullable=False, trim=True)

    def get(self):
        # 로직
        result = 'group'
        return result, 200

    @nsUser.expect(user)  # 요청될 body model
    @nsUser.response(200, {"email":"String","nickname":"Nickname"})  # 반환될 값
    def post(self):

        data = UserController.requestParser.parse_args()

        userRequest = UserRequest(data)
        userService = UserService()
        result = userService.save(userRequest)
        return UserResponse(result).__dict__, 201


@nsUser.route("/<int:uesr_id>")
class UserSingleController(Resource):
    def get(self, user_id):
        # 로직
        result = user_id
        return result, 200

    def delete(self, user_id):
        userService = UserService()
        userService.deleteById(user_id)

        return Response(status=204)
