from io import BytesIO

from flask import Flask, session
from PIL import Image

from myapp import db
from myapp.entity import Photo

from myapp.configs import s3_connection


BUCKET_NAME="blossom"

def save_photo_to_db():
    instance=Photo(photo_id=111, name="123",fileFormat="qwe",user=2)
    db.session.add(instance)
    db.seesion.commit()


# s3에 이미지 저장, 조회, 삭제 / ai 이미지 변환
def upload_photos(file):
    s3_path='test/123'
    s3 = s3_connection()
    bucket = s3.Bucket(BUCKET_NAME)
    s3.Bucket(BUCKET_NAME).put_object(
        Body=file,
        Key=s3_path,
        ContentType=file.content_type
    )

    location = s3.get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
    image_url = f'https://{BUCKET_NAME}.s3.{location}.amazonaws.com/{s3_path}'

    image_info={}

    image_info['filename']='test'
    image_info['url']=image_url

    return image_info


def get_photos_by_userid(user_id):
    obj=Photo.query.filter_by(user=user_id)
    #objs=session.query(Photo.name).filter_by(user=user_id)
    print(obj)

    return obj


def get_photo_from_bucket(filename):
    target = bucket.Object('test')
    response = target.get()
    return response


def delete_photos_by_id(id_list):
    # s3 삭제

    # rds 삭제
    targets=Photo.query.filter_by(photo_id__in=id_list)
    session.delete(targets)
    session.commit()
    pass
