from flask_restful import Resource, reqparse
from myapp.entity.Entity import User
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
        try:
            user_data = User.query.filter_by(email=data['email']).first()
            if user_data is not None:
                return "This email is already exist", 400
            userRequest = UserRequest(data)
            userService = UserService()
            result = userService.save(userRequest)
            return result, 201
        except Exception as e:
            print(str(e))
            return str(e), 400

    def delete(self):
        data = UserController.saveRequest.parse_args()
        try:
            user_data = User.query.filter_by(username=data['email']).first()
            if user_data is None:
                return "This email is not exist", 400
            else:
                UserService().delete((UserRequest(data)))
                return "Delete successful", 201
        except Exception as e:
            print(str(e))
            return str(e), 400


class UserSingleController(Resource):
    def get(self, user_id):
        # 로직
        result = user_id
        return result, 200