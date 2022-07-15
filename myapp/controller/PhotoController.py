from io import BytesIO

from flask import request, send_file, Response, session
from flask_restful import Resource

from myapp.entity import Photo
from myapp.service.PhotoService import delete_photos_by_id, upload_photos_to_s3, save_photo_to_db, \
    get_photos_from_bucket_by_userid

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, pil_img.format, quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/' + pil_img.format)


class PhotoController(Resource):
    def get(self):  # user_id 로 사진 겟할때
        user_id = request.args.get('userId')
        get_photos_from_bucket_by_userid(user_id)
        return {'dd': f'dd{user_id}'}

    def post(self):
        try:
            reqFile = request.files['file']
            photo_id = save_photo_to_db(reqFile.filename, reqFile.content_type, user_id=1)
            upload_photos_to_s3(reqFile, photo_id)
            return Response("good", status=200)
        except:
            return Response("file form-data가 존재하지 않습니다.", status=400)


    def delete(self):
        targets = request.get_json()
        delete_photos_by_id(targets['id'])
        return Response(targets, status=204)


class ColorizedPhoto(Resource):
    def get(self, id):
        # 컬러복원된 사진 조회
        pass

