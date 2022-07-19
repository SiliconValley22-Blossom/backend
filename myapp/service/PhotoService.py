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


def savePhoto(file, userId):
    fileFormat = file.content_type.split("/")[1]

    # DB에 file 정보 저장
    color_uuid = str(uuid.uuid4()) + "." + fileFormat
    instance_color = Photo(name="color_" + file.filename, fileFormat=file.content_type, user=userId, url=color_uuid)

    db.session.add(instance_color)
    db.session.commit()
    db.session.refresh(instance_color)

    black_uuid = str(uuid.uuid4()) + "." + fileFormat
    instance_black = Photo(name=file.filename, fileFormat=file.content_type, user=userId, url=black_uuid,
                           color_id=instance_color.photo_id)
    db.session.add(instance_black)

    # s3 흑백사진 저장
    uploadPhotosToS3(file, fileFormat, black_uuid, "black")

    db.session.commit()
    # ai 셀러리 요청 (그 다음은 비동기처리)
    colorized.delay(black_uuid, color_uuid, fileFormat)


@app.task
def colorized(blackPhotoId, colorPhotoId, fileFormat):
    blackImage = bucket.Object(f'black/{blackPhotoId}.{fileFormat}').get()['Body']

    upload = {'file': imageToByte(blackImage, fileFormat)}

    colorImage = requests.post(COLORIZED_API, files=upload)
    uploadPhotosToS3(colorImage.content, fileFormat, colorPhotoId, 'color')


def uploadPhotosToS3(file, fileFormat, p_uuid, flag):
    s3_Key = f'{flag}/{p_uuid}.{fileFormat}'

    bucket.put_object(
        Body=file,
        Key=s3_Key,
        ContentType=fileFormat
    )


def getPhotosFromBucketByUserId(user_id):
    # target_user = User.query.filter(User.user_id.in_(user_id)).all()
    sql_query = "select p1.url as black_url, p2.url as color_url \
        from photo p1 join photo p2 \
        where p1.user=1 and p1.is_deleted=0 and p1.color_id=p2.photo_id \
        order by p1.created_at desc"
    cursor = db.session.execute(sql_query)

    results = cursor.fetchall()  # (흑백사진 url, 컬러사진 url)
    results = [list(row) for row in results]

    return {"url_list": results}


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
    dic={"url":str(target)}
    return dic
