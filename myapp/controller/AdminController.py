from flask import request, jsonify
from flask_restx import Resource, Namespace

from myapp.service.AdminService import AdminService

nsAdmin = Namespace('api/admin')


@nsAdmin.route('/users/list')
class AdminUserController(Resource):
    def get(self):
        page = request.args.get('page', type=int, default=1)
        adminService = AdminService()
        result = adminService.getAllUsers(page)
        return jsonify(result)

    def delete(self):
        id_list = request.json.get('id_list')
        adminService = AdminService()
        adminService.deleteUserForcefully(id_list)
        return 204