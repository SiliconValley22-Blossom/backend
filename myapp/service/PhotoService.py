import requests
from sqlalchemy import and_
from flask import request, send_file
from myapp import db
from myapp.entity import Photo, User

from myapp.configs import s3_connection, BUCKET_NAME

s3 = s3_connection()
bucket = s3.Bucket(BUCKET_NAME)
reqUrl = "http://localhost:5555/image"


def savePhotoToDB(name, fileFormat, user_id):
    # db 저장 -> pk 반환
    target_user = User.query.filter_by(user_id=user_id)
    instance = Photo(name=name, fileFormat=fileFormat, user=user_id)
    db.session.add(instance)
    db.session.commit()

    db.session.refresh(instance)
    print(instance.photo_id)

    return instance.photo_id


def uploadPhotosToS3(file, photo_id):
    s3_Key = f'test/{photo_id}.{file.filename}.{file.content_type}'

    bucket.put_object(
        Body=file,
        Key=s3_Key,
        ContentType=file.content_type
    )


def getPhotosFromBucketByUserId(user_id):
    # target_user = User.query.filter(User.user_id.in_(user_id)).all()
    objs = Photo.query.filter(and_(Photo.user == user_id, Photo.is_deleted == False)).with_entities(
        Photo.photo_id).all()
    print(objs)

    return


def deletePhotosById(id_list):
    targets = Photo.query.filter(Photo.photo_id.in_(id_list))
    # s3 삭제
    for instance in targets.all():
        instance.is_deleted = True
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

    # targets.delete()
    db.session.commit()


def postBlackImage(reqFile):
    upload={'file':reqFile}
    return requests.post(reqUrl, files=upload)


def serve_pil_image(np_img, format):
    #pil_img = Image.fromarray((np_img * 255).astype(np.uint8))
    img_io = BytesIO()
    pil_img.save(img_io, format, quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/' + format)