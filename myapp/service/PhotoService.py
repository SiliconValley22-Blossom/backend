import uuid
from io import BytesIO
import requests
from PIL import Image
from celery import Celery
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
    color_uuid = 'color/' + str(uuid.uuid4()) + "." + fileFormat
    instance_color = Photo(name="color_" + file.filename, file_format=file.content_type, user=userId, url=color_uuid)

    db.session.add(instance_color)
    db.session.commit()
    db.session.refresh(instance_color)

    black_uuid = 'black/' + str(uuid.uuid4()) + "." + fileFormat
    instance_black = Photo(name=file.filename, file_format=file.content_type, user=userId, url=black_uuid,
                           color_id=instance_color.photo_id)
    db.session.add(instance_black)
    db.session.commit()
    db.session.refresh(instance_black)

    # s3 흑백사진 저장
    uploadPhotosToS3(file, fileFormat, black_uuid)

    # ai 셀러리 요청 (그 다음은 비동기처리)
    colorized.delay(black_uuid, color_uuid, fileFormat)

    return {"black_photo_id": instance_black.photo_id,
            "color_photo_id": instance_color.photo_id}


@app.task
def colorized(blackPhotoId, colorPhotoId, fileFormat):
    blackImage = bucket.Object(f'black/{blackPhotoId}.{fileFormat}').get()['Body']

    upload = {'file': imageToByte(blackImage, fileFormat)}

    colorImage = requests.post(COLORIZED_API, files=upload)
    uploadPhotosToS3(colorImage.content, fileFormat, colorPhotoId, 'color')


def uploadPhotosToS3(file, fileFormat, p_uuid):
    s3_Key = f'{p_uuid}.{fileFormat}'

    bucket.put_object(
        Body=file,
        Key=s3_Key,
        ContentType=fileFormat
    )


def getPhotosFromBucketByEmail(email):
    sql_query = f"SELECT p1.url AS black_url, p2.url AS color_url \
                  FROM photo p1 JOIN photo p2 \
                  WHERE p1.user=(SELECT user_id FROM user WHERE email='{email}')\
                        and p1.is_deleted=0 and p1.color_id=p2.photo_id\
                  ORDER BY p1.created_at DESC"
    cursor = db.session.execute(sql_query)

    results = cursor.fetchall()  # (흑백사진 url, 컬러사진 url)
    results = [list(row) for row in results]

    return {"photo_list": results}


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
    return requests.post(COLORIZED_API, files=upload)


def imageToByte(image_file, format):
    print(image_file)
    image = Image.open(image_file)
    buffer = BytesIO()
    image.save(buffer, format, quality=70)
    buffer.seek(0)
    print(buffer)
    return buffer


def getPhotoByPhotoId(photo_id):
    target = Photo.query.filter(and_(Photo.is_deleted == False, Photo.photo_id == photo_id)).with_entities(
        Photo.url).first()[0]
    dic = {"photo": str(target)}
    return dic
