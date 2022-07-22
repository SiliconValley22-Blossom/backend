from datetime import timedelta

from flask import jsonify, make_response
from werkzeug.exceptions import Unauthorized

from myapp import jwt_redis
from myapp.entity import User
import jwt
from flask_jwt_extended import (
    create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_csrf_token,
    get_jwt_identity, get_jwt
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

            jwt_redis.set(loginRequest.email, refresh_token, ex=timedelta(days=14))

            return access_token, refresh_token

        raise Unauthorized(www_authenticate="/api/login", description="wrong password")

    def logout(self):
        current_user = get_jwt_identity()
        user = get_jwt()['jti']
        resp = jsonify({'msg': 'Logout successfully'})
        jwt_redis.set(current_user, "", ex=timedelta(hours=1))
        # 쿠키 삭제
        #resp.set_cookie('access_token_cookie', '', expires=0)
        #resp.set_cookie('refresh_token_cookie', '', expires=0)
        # 쿠키 변경
        set_access_cookies(resp,'')
        set_refresh_cookies(resp,'')
        return resp

    # def logout(self, loginRequest):
    #     user = User(email=userRequest.email,
    #                 password=userRequest.password,
    #                 nickname=userRequest.nickname,
    #                 check__deleted=1)
    #
    #     db.session.add(user)
    #     db.session.commit()
    #     return user