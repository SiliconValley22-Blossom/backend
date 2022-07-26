import json

from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse
from myapp.entity.Entity import User
from myapp.service import UserService
from flask_restx import Namespace, fields, Resource

nsUser = Namespace('api/users')
user = nsUser.model('User', {
    'email': fields.String,
    'password': fields.String,
    'nickname': fields.String
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

    #@jwt_required(locations=['cookies'])
    def get(self):
        '''비밀번호 user 이메일로 전송'''
        #curUser = get_jwt_identity()
        userService = UserService()
        resp = userService.sendPassword('1')
        return resp

    @nsUser.expect(user)  # 요청될 body model
    @nsUser.response(200, {"email": "String", "nickname": "Nickname"})  # 반환될 값
    def post(self):
        data = UserController.requestParser.parse_args()
        userRequest = UserRequest(data)
        userService = UserService()
        result = userService.save(userRequest)
        return UserResponse(result).__dict__, 201

    @jwt_required(locations=['cookies'])
    def patch(self):
        data = request.json
        curUser = get_jwt_identity()
        userService = UserService()
        resp = userService.modifyPassword(curUser, data)
        return resp


@nsUser.route("/<int:uesr_id>")
class UserSingleController(Resource):
    def delete(self, user_id):
        userService = UserService()
        userService.deleteById(user_id)

        return Response(status=204)
