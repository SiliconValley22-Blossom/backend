from io import BytesIO

from flask import request, send_file, Response, session
from flask_restful import Resource

from myapp.entity import Photo
from myapp.service.PhotoService import get_photos_by_userid, delete_photos_by_id, upload_photos

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def serve_pil_image(pil_img):
    img_io = BytesIO()
    pil_img.save(img_io, pil_img.format, quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/' + pil_img.format)


class PhotoController(Resource):
    def get(self):
        # userId에 해당하는 사진 조회
        # RDS에 userid에 해당하는 사진 링크받아오기
        # 컬러화된 사진만 리턴?
        user_id=request.args.get('userId')
        get_photos_by_userid(user_id)
        return {'dd':f'dd{user_id}'}

    def post(self):
        # 사진 s3에 저장
        # 링크 받아서 RDS에 저장

        f=request.files['file']
        #photo_info=upload_photos(f)
        a=Photo.query.filter_by(user=1)
        print(a[0].name)

        return Response("123",status=200)

    def delete(self): # 보류
        # body로 삭제할 아이디 리스트 받음 [1,4,5...]
        targets=request.get_json()
        print(type(targets['id']))
        delete_photos_by_id(targets['id'])
        return targets


class ColorizedPhoto(Resource):
    def get(self,id):
        # 컬러복원된 사진 조회
        pass


'''
@photo.route('/image', methods=['GET', 'POST'])
def _post():
    if request.method == "POST":
        file = request.files['file']

        s3.Bucket(BUCKET_NAME).put_object(
            Body=file,
            Key="test/" + file.name,
            ContentType=file.content_type
        )
        response = 201
        return response
    elif request.method == 'GET':
        bucket = s3.Bucket(BUCKET_NAME)
        filename = "newFile.png"
        object = bucket.Object(f'test/{filename}')
        response = object.get()
        file_stream = response['Body']
        img = Image.open(file_stream)

        return serve_pil_image(img)


@photo.route('/', methods=['GET']) # 컬러화된 모든 사진들 출력
def get_all():
    posts=get_all_posts()


'''