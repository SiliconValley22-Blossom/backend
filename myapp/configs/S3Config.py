import boto3
import os

BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.environ.get('S3_ID')
AWS_SECERET_ACCESS_KEY = os.environ.get('S3_SECRET_KEY')


def s3_connection():
    s3 = boto3.resource(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECERET_ACCESS_KEY,
    )
    return s3
