from flask import request, Response, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, fields
from flask_restx import Resource

from myapp.service.PhotoService import deletePhotosById, savePhoto, \
    getPhotosFromBucketByEmail, getPhotoByPhotoId, getPhotosFromBucketByUserId

nsPhoto = Namespace('api/photos')
idList = nsPhoto.model('Id', {
    'id_list': fields.List(fields.Integer)
})


@nsPhoto.route('')
class PhotoController(Resource):
    @jwt_required(locations=['cookies'])
    @nsPhoto.param("userId", "Id에 해당하는 사진 조회 / 토큰으로 사진 조회", type=int)
    @nsPhoto.response(200, "", nsPhoto.model('GetPhotos', {'photo_list': fields.List(fields.Integer)}))
    def get(self):
        """User ID에 해당하는 사진을 조회"""
        param = request.args.get('userId')
        if param is None:
            email = get_jwt_identity()
            result = getPhotosFromBucketByEmail(email)
            resp = jsonify({'photo_list': result})
        else:
            result = getPhotosFromBucketByUserId(param)
            resp = jsonify({'photo_list': result})

        return resp

    @jwt_required(locations=['cookies'])
    @nsPhoto.response(201, "", nsPhoto.model('PostPhoto', {
        "black_photo_id": fields.Integer,
        "color_photo_id": fields.Integer
    }))
    def post(self):
        """요청받은 흑백사진을 저장하고 컬러화 진행"""
        curUser = get_jwt_identity()
        reqFile = request.files['file']
        result = savePhoto(reqFile, curUser)
        resp = jsonify(result)
        resp.status = 201
        return resp

    @jwt_required(locations=['cookies'])
    @nsPhoto.expect(idList)
    @nsPhoto.response(204, "", idList)
    def delete(self):
        """Id 리스트에 있는 사진들을 삭제 처리"""
        idList = request.get_json()['id']
        deletePhotosById(idList)
        return Response(idList, status=204)


@nsPhoto.route('/<int:photo_id>')
class PhotoSingleController(Resource):
    @jwt_required(locations=['cookies'])
    @nsPhoto.response(200, "", nsPhoto.model('GetPhoto', {'photo': fields.Integer}))
    def get(self, photo_id):
        """photo_id에 해당하는 사진 단일 조회"""
        resp = getPhotoByPhotoId(photo_id)
        return resp
