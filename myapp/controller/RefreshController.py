from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, set_access_cookies
from flask_restx import Namespace, Resource

from myapp.service.TokenService import TokenService

nsRefresh = Namespace('api/refresh')


@nsRefresh.route("")
class RefreshController(Resource):
    @jwt_required(locations=['cookies'], refresh=True)
    @nsRefresh.response(200, 'Access token has recreated')
    def get(self):
        '''refresh token 재발급'''
        curUser = get_jwt_identity()
        refreshToken = request.cookies.get('refresh_token_cookie')

        tokenService = TokenService()
        newToken = tokenService.recreateAccessToken(curUser, refreshToken)
        resp = jsonify({
            'message': 'Access token has recreated'
        })
        set_access_cookies(resp, newToken)
        resp.status = 200

        return resp
