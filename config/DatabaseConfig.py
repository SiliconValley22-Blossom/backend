DB_USERNAME = 'root'
DB_PASSWORD = '1234'
DB_HOST = 'localhost'
DB_SCHEMA = 'blossom'
DB_PORT = '3306'

SQLALCHEMY_TRACK_MODIFICATIONS = False


def getURI():
    return 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(DB_USERNAME, DB_PASSWORD,
                                                                DB_HOST, DB_PORT, DB_SCHEMA)