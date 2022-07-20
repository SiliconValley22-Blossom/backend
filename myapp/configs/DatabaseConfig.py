import os

DB_USERNAME = os.environ.get('RDS_NAME')
DB_PASSWORD = os.environ.get('RDS_PASSWORD')
DB_HOST = os.environ.get('RDS_ENDPOINT')
DB_SCHEMA = os.environ.get('RDS_DATABASE')
DB_PORT = os.environ.get('RDS_PORT')

SQLALCHEMY_TRACK_MODIFICATIONS = False


def getURI():
    return 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USERNAME, DB_PASSWORD,
                                                                DB_HOST, DB_PORT, DB_SCHEMA)