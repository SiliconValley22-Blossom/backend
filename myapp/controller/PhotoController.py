from io import BytesIO

from flask import request, send_file, Response, session
from flask_restful import Resource

from myapp.entity import Photo
from myapp.service.PhotoService import deletePhotosById, uploadPhotosToS3, savePhotoToDB, \
    getPhotosFromBucketByUserId, postBlackImage

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, pil_img.format, quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/' + pil_img.format)


class PhotoController(Resource):
    def get(self):  # user_id 로 사진 겟할때
        user_id = request.args.get('userId')
        getPhotosFromBucketByUserId(user_id)
        return {'dd': f'dd{user_id}'}

    def post(self):
        try:
            reqFile = request.files['file']
            photo_id = savePhotoToDB(reqFile.filename, reqFile.content_type, user_id=1)
            upload_photos_to_s3(reqFile, photo_id)
            return Response("good", status=200)
        except:
            return Response("file form-data가 존재하지 않습니다.", status=400)

    def delete(self):
        targets = request.get_json()
        deletePhotosById(targets['id'])
        return Response(targets, status=204)


class ColorizedPhoto(Resource):
    def get(self, photoId):
        # 컬러복원된 사진 조회
        pass

    def post(self, photoId):
        # 흑백 사진 컬러사진 복원 후 response
        reqFile = request.files['file']
        return Response(postBlackImage(reqFile), content_type='image/jpeg')