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

    def post(self):
        data = LoginController.saveRequest.parse_args()
        try:
            user_email = data['email']
            user_password = data['password']
            # 이메일 및 비밀번호 존재 여부 확인
            if user_email is None:
                return "User Not Found", 404

            # 데이터베이스에 있는 정보랑 비교
            # 일치하면 로그인 성공
            # 다른 페이지 접속 시 jwt를 통한 접근
            user_data = User.query.filter_by(email=data['email']).first()
            if user_data is not None:
                return "username is already exist", 400
            userRequest = UserRequest(data)
            userService = UserService()
            result = userService.save(userRequest)
            return result, 201
        except Exception as e:
            print(str(e))
            return str(e), 400

