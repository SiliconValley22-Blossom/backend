import uuid
from io import BytesIO
import requests
from PIL import Image
from celery import Celery
from flask import jsonify
from sqlalchemy import and_

from myapp import db
from myapp.configs import s3_connection, BUCKET_NAME
from myapp.entity import Photo

from myapp.configs import COLORIZED_API, RBMQ_CONNECTION_URI

s3 = s3_connection()
bucket = s3.Bucket(BUCKET_NAME)

app = Celery('tasks',
             broker=RBMQ_CONNECTION_URI)


def savePhoto(file, email):
    fileFormat = file.content_type.split("/")[1]
    sql = f"SELECT user_id \
            FROM user \
            WHERE email='{email}'"
    cursor = db.session.execute(sql)
    userId = cursor.fetchall()[0][0]

    # DB에 file 정보 저장
    colorUuid = 'color/' + str(uuid.uuid4()) + "." + fileFormat
    instanceColor = Photo(name="color_" + file.filename, file_format=file.content_type, user=userId, url=colorUuid)

    db.session.add(instanceColor)
    db.session.commit()
    db.session.refresh(instanceColor)

    blackUuid = 'black/' + str(uuid.uuid4()) + "." + fileFormat
    instanceBlack = Photo(name=file.filename, file_format=file.content_type, user=userId, url=blackUuid,
                           color_id=instanceColor.photo_id)
    db.session.add(instanceBlack)
    db.session.commit()
    db.session.refresh(instanceBlack)

    # s3 흑백사진 저장
    uploadPhotosToS3(file, fileFormat, blackUuid)

    # ai 셀러리 요청 (그 다음은 비동기처리)
    colorized.delay(blackUuid, colorUuid, fileFormat)

    resp = jsonify({
        "black_photo_id": instanceBlack.photo_id,
        "color_photo_id": instanceColor.photo_id
    })
    return resp

@app.task
def colorized(blackPhotoId, colorPhotoId, fileFormat):
    blackImage = bucket.Object(f'{blackPhotoId}').get()['Body']

    upload = {'file': imageToByte(blackImage, fileFormat)}

    colorImage = requests.post(COLORIZED_API, files=upload)
    uploadPhotosToS3(colorImage.content, fileFormat, colorPhotoId)


def uploadPhotosToS3(file, fileFormat, uuid):
    s3Key = f'{uuid}'

    bucket.put_object(
        Body=file,
        Key=s3Key,
        ContentType=fileFormat
    )


def getPhotosFromBucketByEmail(email):
    sql = f"SELECT p1.url AS black_url, p2.url AS color_url \
                  FROM photo p1 JOIN photo p2 \
                  WHERE p1.user=(SELECT user_id FROM user WHERE email='{email}')\
                        and p1.is_deleted=0 and p1.color_id=p2.photo_id\
                  ORDER BY p1.created_at DESC"
    cursor = db.session.execute(sql)

    results = cursor.fetchall()  # (흑백사진 url, 컬러사진 url)
    results = [list(row) for row in results]
    return results


def getPhotosFromBucketByUserId(userId):
    sql = f'SELECT p1.url AS black_url, p2.url AS color_url \
                  FROM photo p1 JOIN photo p2 \
                  WHERE p1.user={userId}\
                        and p1.is_deleted=0 and p1.color_id=p2.photo_id\
                  ORDER BY p1.created_at DESC'
    cursor = db.session.execute(sql)

    results= cursor.fetchall()
    results = [list(row) for row in results]
    return results


def deletePhotosById(idList):
    targets = Photo.query.filter(Photo.photo_id.in_(idList))
    # s3 삭제
    for instance in targets.all():
        instance.is_deleted = True
    db.session.commit()


def postBlackImage(reqFile):
    upload = {'file': reqFile}
    return requests.post(COLORIZED_API, files=upload)


def imageToByte(imageFile, format):
    print(imageFile)
    image = Image.open(imageFile)
    buffer = BytesIO()
    image.save(buffer, format, quality=70)
    buffer.seek(0)
    print(buffer)
    return buffer


def getPhotoByPhotoId(photoId):
    target = Photo.query.filter(and_(Photo.is_deleted == False, Photo.photo_id == photoId)).with_entities(
        Photo.url).first()
    if target:
        target = target[0]
    result = jsonify({"photo": target})
    return result
