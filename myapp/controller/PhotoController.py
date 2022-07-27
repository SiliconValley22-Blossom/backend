from flask import request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, set_access_cookies
from flask_restx import Namespace
from flask_restx import Resource

from myapp.service.PhotoService import deletePhotosById, savePhoto, \
    getPhotosFromBucketByEmail, getPhotoByPhotoId

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

nsPhoto = Namespace('api/photos')


@nsPhoto.route('')
class PhotoController(Resource):
    @jwt_required(locations=['cookies'])
    def get(self):
        """User ID에 해당하는 사진을 조회한다."""
        email = get_jwt_identity()
        url_list = getPhotosFromBucketByEmail(email)
        return url_list

    @jwt_required(locations=['cookies'])
    def post(self):
        """클라이언트로부터 요청받은 흑백사진을 저장하고 컬러화한다."""
        curUser = get_jwt_identity()
        reqFile = request.files['file']
        result = savePhoto(reqFile, curUser)
        resp = jsonify(result)
        resp.status = 201
        return resp

    @jwt_required(locations=['cookies'])
    def delete(self):
        """요청받은 사진을 삭제 처리한다."""
        id_list = request.get_json()['id']
        deletePhotosById(id_list)
        return Response(id_list, status=204)


@nsPhoto.route('/<int:photo_id>')
class PhotoSingleController(Resource):
    @jwt_required(locations=['cookies'])
    def get(self, photo_id):
        """photo_id에 해당하는 사진 단일 조회"""
        result = getPhotoByPhotoId(photo_id)
        resp = jsonify(result)
        return resp, 200


'''
422 : "Signature verification failed"

'''
