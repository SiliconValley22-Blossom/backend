from flask_jwt_extended import create_access_token

from myapp import jwtRedis


class TokenService:
    def recreateAccessToken(self, email, refresh):
        target = jwtRedis.get(refresh)
        if target == email:
            newToken = create_access_token(identity=email)
            return newToken