from myapp import db
from myapp.entity import User
from flask_bcrypt import Bcrypt
from flask import Flask
import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)

class LoginService:
    def login(self, loginRequest):
        user = User.query.filter_by(email=loginRequest.email).first()
        if not user:
            return {
                       "message": "User Not Found"
                   }, 404
        else:
            # 암호화 후 비밀번호 비교하여 일치하면 토큰 발행
            if bcrypt.check_password_hash(user.password, 'loginRequest.password'):
                return {
                           'Authorization': jwt.encode({'name': user.nickname}, "secret", algorithm="HS256")
                           # str으로 반환하여 return
                       }, 200
            else:
                return {
                       "message": "Auth Failed"
                   }, 500


    # def logout(self, loginRequest):
    #     user = User(email=userRequest.email,
    #                 password=userRequest.password,
    #                 nickname=userRequest.nickname,
    #                 check__deleted=1)
    #
    #     db.session.add(user)
    #     db.session.commit()
    #     return user