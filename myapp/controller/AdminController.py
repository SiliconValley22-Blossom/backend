from flask import request, jsonify
from flask_jwt_extended import jwt_required
from flask_restx import Resource, Namespace, fields

from myapp.service.AdminService import AdminService

nsAdmin = Namespace('api/admin')


@nsAdmin.route('/users')
class AdminUserController(Resource):
    @jwt_required(locations=['cookies'])
    @nsAdmin.response(200,"모든 회원 조회",{"user":"user"})
    def get(self):
        page = request.args.get('page', type=int, default=1)
        adminService = AdminService()
        result = adminService.getAllUsers(page)
        return jsonify(result)

    def delete(self):
        idList = request.json.get('id_list')
        adminService = AdminService()
        adminService.deleteUserForcefully(idList)
        return 204