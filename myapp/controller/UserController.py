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
       # try:
           # user_data = User.query.filter_by(username=data['username']).first()
        userRequest = UserRequest(data)
        userService = UserService()
        result = userService.save(userRequest)
        return result, 201
        #except Exception as e:
         #   print(str(e))
          #  return str(e), 400

    def delete(self):
        data = UserController.saveRequest.parse_args()
        try:
            user_data = User.query.filter_by(username=data['username']).first()
            if user_data is not None:
                return "username is not exist", 400
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