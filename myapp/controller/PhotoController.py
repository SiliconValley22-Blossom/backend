from flask import request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask_restx import Namespace
from flask_restx import Resource

from myapp.service.PhotoService import deletePhotosById, savePhoto, \
    getPhotosFromBucketByEmail, getPhotoByPhotoId, getPhotosFromBucketByUserId

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

nsPhoto = Namespace('api/photos')


@nsPhoto.route('')
class PhotoController(Resource):
    def get(self):
        """User ID에 해당하는 사진을 조회"""
        param = request.args.get('userId')
        if param is None:
            if verify_jwt_in_request(locations=['cookies']):
                email = get_jwt_identity()
                result = getPhotosFromBucketByEmail(email)
                resp = jsonify({'photo_list': result})
        else:
            result = getPhotosFromBucketByUserId(param)
            resp = jsonify({'photo_list': result})

        return resp

    @jwt_required(locations=['cookies'])
    def post(self):
        """요청받은 흑백사진을 저장하고 컬러화 진행"""
        curUser = get_jwt_identity()
        reqFile = request.files['file']
        result = savePhoto(reqFile, curUser)
        resp = jsonify(result)
        resp.status = 201
        return resp

    @jwt_required(locations=['cookies'])
    def delete(self):
        """Id 리스트에 있는 사진들을 삭제 처리"""
        idList = request.get_json()['id']
        deletePhotosById(idList)
        return Response(idList, status=204)


@nsPhoto.route('/<int:photo_id>')
class PhotoSingleController(Resource):
    @jwt_required(locations=['cookies'])
    def get(self, photo_id):
        """photo_id에 해당하는 사진 단일 조회"""
        resp = getPhotoByPhotoId(photo_id)
        return resp
