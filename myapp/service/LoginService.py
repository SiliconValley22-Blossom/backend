from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity, get_jwt
)
from werkzeug.exceptions import Unauthorized

from myapp import jwt_redis
from myapp.entity import User
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

            jwt_redis.set(refresh_token, loginRequest.email, ex=timedelta(days=14))

            return access_token, refresh_token

        raise Unauthorized(www_authenticate="/api/login", description="wrong password")

    def logout(self,refresh):
        resp = jsonify({'msg': 'Logout successfully'})
        jwt_redis.delete(refresh)

        return resp