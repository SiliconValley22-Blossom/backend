import logging, boto3, pymysql

from flask import Flask



RDS_HOST = 'localhost'
RDS_DATABASE = 'test_blossom'
RDS_USER = 'root'
RDS_PASSWORD = '123qwe'
DB_PORT = 3306


def db_connection():
    try:
        db = pymysql.connect(
            host=RDS_HOST,
            user=RDS_USER,
            db=RDS_DATABASE,
            password=RDS_PASSWORD,
            charset='utf8'
        )
        cursor = db.cursor()
        return db, cursor
    except:
        logging.error("DB에 연결되지 않았습니다.")


BUCKET_NAME = "blossom"
AWS_ACCESS_KEY_ID = "."
AWS_SECERET_ACCESS_KEY = "."


def s3_connection():
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECERET_ACCESS_KEY,
    )
    return s3
