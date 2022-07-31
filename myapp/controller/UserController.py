from flask import Response, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse
from flask_restx import Namespace, fields, Resource

from myapp.service import UserService

nsUser = Namespace('api/users')

user = nsUser.model('User', {
    'email': fields.String,
    'password': fields.String,
    'nickname': fields.String
})
pw = nsUser.model('password', {
    'password': fields.String,
    'new_password': fields.String
})
respUser = nsUser.model('respUser', {
    'user_id': fields.Integer,
    'email': fields.String,
    'nickname': fields.String
})
respUserInfo = nsUser.model('respUserInfo', {
    'user_id': fields.Integer,
    'email': fields.String,
    'nickname': fields.String,
    'created_at': fields.DateTime,
    'updated_at': fields.DateTime,
    'is_deleted': fields.Boolean
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

    @jwt_required(locations=['cookies'])
    @nsUser.response(200, "회원 정보 조회", respUserInfo)  # 반환될 값
    def get(self):
        '''회원 정보 조회'''
        curUser = get_jwt_identity()
        userService = UserService()
        result = userService.getUserInfo(curUser)
        return result

    @nsUser.expect(user)  # 요청될 body model
    @nsUser.response(201, "회원가입", respUser)  # 반환될 값
    def post(self):
        '''회원 회원가입'''
        data = UserController.requestParser.parse_args()
        userRequest = UserRequest(data)
        userService = UserService()
        result = userService.save(userRequest)
        return UserResponse(result).__dict__, 201

    @jwt_required(locations=['cookies'])
    @nsUser.expect(pw)
    @nsUser.response(200, "비밀번호 변경되었습니다.")
    def patch(self):
        '''회원 비밀번호 변경'''
        data = request.json
        curUser = get_jwt_identity()
        userService = UserService()
        resp = userService.modifyPassword(curUser, data)
        return resp


@nsUser.route("/<int:uesr_id>")
class UserSingleController(Resource):
    @jwt_required(locations=['cookies'])
    @nsUser.response(204, "회원 정보 삭제 처리")
    def delete(self, user_id):
        '''user_id에 해당하는 회원 삭제 처리'''
        userService = UserService()
        userService.deleteById(user_id)

        return Response(status=204)


@nsUser.route('/reset-pw')
class UserPwController(Resource):
    @jwt_required(locations=['cookies'])
    @nsUser.response(200, "회원님의 이메일로 비밀번호를 전송하였습니다.")
    def post(self):
        '''임시 비밀번호를 회원 이메일로 전송'''
        curUser = get_jwt_identity()
        userService = UserService()
        resp = userService.sendPassword(curUser)
        return resp