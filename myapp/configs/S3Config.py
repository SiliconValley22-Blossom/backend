import boto3

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
