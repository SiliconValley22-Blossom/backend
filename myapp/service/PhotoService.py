from myapp import db
from myapp.entity import Photo, User

from myapp.configs import s3_connection

BUCKET_NAME = "blossom"
s3 = s3_connection()
bucket = s3.Bucket(BUCKET_NAME)


def save_photo_to_db(name, fileformat, user_id):
    # db 저장 -> pk 반환
    target_user = User.query.filter_by(user_id=user_id)
    instance = Photo(name=name, fileFormat=fileformat, user=user_id)
    db.session.add(instance)
    db.session.commit()

    db.session.refresh(instance)
    print(instance.photo_id)

    return instance.photo_id


def upload_photos_to_s3(file, photo_id):
    s3_path = f'img/{photo_id}'

    s3.Bucket(BUCKET_NAME).put_object(
        Body=file,
        Key=s3_path,
        ContentType=file.content_type
    )

    location = s3.get_bucket_location(Bucket=BUCKET_NAME)['LocationConstraint']
    image_url = f'https://{BUCKET_NAME}.s3.{location}.amazonaws.com/{s3_path}'

    image_info = dict()

    image_info['filename'] = 'test'
    image_info['url'] = image_url

    return image_info


def get_photos_by_userid(user_id):
    obj = Photo.query.filter_by(user=user_id).all()  # list
    result = []
    result.append(obj[i].photo_id for i in range(len(obj)))

    return result


def get_photo_from_bucket(filename):
    return


def delete_photos_by_id(id_list):
    targets = Photo.query.filter_by(photo_id__in=id_list).all()  # list

    # s3 삭제
    for key in id_list:
        bucket.delete_objects(
            Delete={
                'Objects':[
                    {
                    'key': f'{str(key)}'
                    }
                ]
            }
        )

    # rds 삭제
    db.session.delete(targets)
    db.session.commit()
    pass
