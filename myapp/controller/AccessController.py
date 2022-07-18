from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import reqparse
from flask_restx import Namespace, Resource

nsAccess = Namespace('api/access')


@nsAccess.route('')
class AccessController(Resource):
    # Request Fields
    saveRequest = reqparse.RequestParser()
    saveRequest.add_argument('email', type=str, nullable=False, trim=True)
    saveRequest.add_argument('password', type=str, nullable=False, trim=True)

    @jwt_required
    def get(self):
        # access 토큰 유효성 확인
        current_user = get_jwt_identity()
        # 서명된 사용자 이메일을 찾음
        return jsonify(logged_in_as=current_user), 200
