from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Resource, Namespace, fields

from myapp.service.AdminService import AdminService

nsAdmin = Namespace('api/admin')

idList = nsAdmin.model('Id', {
    'id_list': fields.List(fields.Integer)
})
user = nsAdmin.model('viewUsers', {
    "user_id": fields.Integer,
    "email": fields.String,
    "nickname": fields.String,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime,
    "is_deleted": fields.Boolean
})


@nsAdmin.route('/users')
class AdminUserController(Resource):
    @jwt_required(locations=['cookies'])
    @nsAdmin.response(200, "모든 회원 조회", user)
    @nsAdmin.response(403, "접근 권한이 없습니다.")
    def get(self):
        """모든 회원 조회"""
        page = request.args.get('page', type=int, default=1)
        curUser = get_jwt_identity()
        adminService = AdminService(curUser)
        result = adminService.getAllUsers(page)
        return jsonify(result)

    @jwt_required(locations=['cookies'])
    @nsAdmin.expect(idList)
    @nsAdmin.response(code=204, description="회원 삭제 처리")
    def delete(self):
        """회원 삭제"""
        idList = request.json.get('id_list')
        curUser = get_jwt_identity()
        adminService = AdminService(curUser)
        adminService.deleteUserForcefully(idList)
        return 204