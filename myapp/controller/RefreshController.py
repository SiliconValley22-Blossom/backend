from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from flask_restful import reqparse
from flask_restx import Namespace, Resource

nsRefresh = Namespace('api/refresh')


@nsRefresh.route("")
class RefreshController(Resource):
    # Request Fields
    requestParser = reqparse.RequestParser()
    requestParser.add_argument('email', type=str, nullable=False, trim=True)
    requestParser.add_argument('password', type=str, nullable=False, trim=True)

    @jwt_required(refresh=True)
    def get(self):
        # refresh token 재발급
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return jsonify(access_token=access_token, current_user=current_user)