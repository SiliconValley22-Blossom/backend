from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token
)
from werkzeug.exceptions import Unauthorized

from myapp import jwtRedis
from myapp.entity import User
from myapp.util import checkPassword


class LoginService:
    def login(self, loginRequest):
        user = User.query.filter_by(email=loginRequest.email).first()
        if not user:
            raise Unauthorized(www_authenticate="/api/login", description="invalid ID")

        isAuth = checkPassword(user.password, loginRequest.password)

        if isAuth:
            accessToken = create_access_token(identity=loginRequest.email)
            refreshToken = create_refresh_token(identity=loginRequest.email)

            jwtRedis.set(refreshToken, loginRequest.email, ex=timedelta(days=14))

            return accessToken, refreshToken

        raise Unauthorized(www_authenticate="/api/login", description="wrong password")

    def logout(self,refresh):
        resp = jsonify({'message': 'Logout successfully'})
        jwtRedis.delete(refresh)

        return resp