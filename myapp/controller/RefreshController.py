from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, set_access_cookies
from flask_restful import reqparse
from flask_restx import Namespace, Resource

from myapp.service.TokenService import TokenService

nsRefresh = Namespace('api/refresh')


@nsRefresh.route("")
class RefreshController(Resource):
    @jwt_required(locations=['cookies'], refresh=True)
    def get(self):
        # refresh token 재발급
        curUser = get_jwt_identity()
        refresh_token = request.cookies.get('refresh_token_cookie')

        tokenService = TokenService()
        new_token = tokenService.recreateAccessToken(curUser, refresh_token)
        resp = jsonify({
            'message': 'Access token is recreated'
        })
        set_access_cookies(resp, new_token)
        resp.status = 200

        return resp
