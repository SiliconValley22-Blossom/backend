from io import BytesIO

from flask import request, send_file, Response, session
from flask_restful import Resource

from myapp.entity import Photo
from myapp.service.PhotoService import deletePhotosById, uploadPhotosToS3, savePhoto, \
    getPhotosFromBucketByUserId, postBlackImage

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


# ns = api.namespace('photos', description='사진 조회,등록,삭제')


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, pil_img.format, quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/' + pil_img.format)


class PhotoController(Resource):
    def get(self):  # user_id에 해당하는 컬러 사진 조회
        user_id = request.args.get('userId')
        url_list = getPhotosFromBucketByUserId(user_id)
        return url_list

    def post(self):
        reqFile = request.files['file']
        savePhoto(reqFile, userId=1)
        return Response("created", status=201)

    def delete(self):
        targets = request.get_json()
        deletePhotosById(targets['id'])
        return Response(targets, status=204)


class ColorizationController(Resource):
    def get(self, photo_id):
        # 컬러복원된 사진 조회
        pass

