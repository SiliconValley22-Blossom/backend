import requests
from sqlalchemy import and_
from flask import request, send_file
from myapp import db
from myapp.entity import Photo, User
from PIL import Image
import uuid

from myapp.configs import s3_connection, BUCKET_NAME

s3 = s3_connection()
bucket = s3.Bucket(BUCKET_NAME)
AI_SERVER_URL = "http://localhost:5555/image"


def savePhoto(file, userId):
    # DB에 file 정보 저장
    black_uuid = uuid.uuid4()
    instance_black = Photo(name=file.filename, fileFormat=file.content_type, user=userId, url=black_uuid, is_black=True)
    db.session.add(instance_black)

    color_uuid = uuid.uuid4()
    instance_color = Photo(name="color_" + file.filename, fileFormat=file.content_type, user=userId, url=color_uuid,
                           is_black=False)
    db.session.add(instance_color)

    # s3 흑백사진 저장
    uploadPhotosToS3(file, black_uuid, "black")

    db.session.commit()
    # ai 셀러리 요청 (그 다음은 비동기처리)


def uploadPhotosToS3(file, p_uuid, flag):
    format = file.content_type.split("/")[1]
    print(format)
    s3_Key = f'{flag}/{p_uuid}.{format}'

    bucket.put_object(
        Body=file,
        Key=s3_Key,
        ContentType=file.content_type
    )


def getPhotosFromBucketByUserId(user_id):
    # target_user = User.query.filter(User.user_id.in_(user_id)).all()
    objs = Photo.query.filter(
        and_(Photo.user == user_id, Photo.is_deleted == False, Photo.is_black == False)).with_entities(
        Photo.url).order_by(Photo.create_at.desc()).all()
    return objs


def deletePhotosById(id_list):
    targets = Photo.query.filter(Photo.photo_id.in_(id_list))
    # s3 삭제
    for instance in targets.all():
        instance.is_deleted = True
        '''
        s3_key = f'test/{instance.photo_id}.{instance.name}.{instance.fileFormat}'
        bucket.delete_objects(
            Delete={
                'Objects': [
                    {
                        'Key': f'{str(s3_key)}'
                    }
                ]
            }
        )
        '''
    # targets.delete()
    db.session.commit()


def postBlackImage(reqFile):
    upload = {'file': reqFile}
    return requests.post(AI_SERVER_URL, files=upload)


def imageToByte(image_file, format):
    image = Image.open(image_file)
    buffer = BytesIO()
    image.save(buffer, format, quality=70)
    buffer.seek(0)
    return buffer
