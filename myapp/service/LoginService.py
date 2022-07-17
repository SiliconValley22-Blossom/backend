from flask import jsonify
from werkzeug.exceptions import Unauthorized
from myapp.entity import User
import jwt
from flask_jwt_extended import (
create_access_token, create_refresh_token
)
from myapp.util import checkPassword


class LoginService:
    def login(self, loginRequest):
        user = User.query.filter_by(email=loginRequest.email).first()
        if not user:
            raise Unauthorized(www_authenticate="/api/login", description="invalid ID")

        isAuth = checkPassword(user.password, loginRequest.password)

        if isAuth:
            access_token = create_access_token(identity=loginRequest.email)
            refresh_token = create_refresh_token(identity=loginRequest.email)
            return access_token, refresh_token

        raise Unauthorized(www_authenticate="/api/login", description="wrong password")


    # def logout(self, loginRequest):
    #     user = User(email=userRequest.email,
    #                 password=userRequest.password,
    #                 nickname=userRequest.nickname,
    #                 check__deleted=1)
    #
    #     db.session.add(user)
    #     db.session.commit()
    #     return user