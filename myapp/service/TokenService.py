from flask import jsonify
from flask_jwt_extended import create_access_token, set_access_cookies

from myapp import jwt_redis


class TokenService:
    def recreateAccessToken(self, email, refresh):
        target = jwt_redis.get(refresh)
        if target == email:
            new_token = create_access_token(identity=email)
            return new_token