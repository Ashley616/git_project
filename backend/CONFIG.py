class Database(object):
    USER = 'root'
    PASSWORD = 'Lalala00'
    NAME = 'recipeRecommdation'

class DatabaseConfig(object):
    ENV = 'development'
    SECRET_KEY = 'f0293u0wef'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{Database.USER}:{Database.PASSWORD}@localhost:3306/{Database.NAME}'
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_TIMEOUT = 10
    SQLALCHEMY_POOL_RECYCLE = 2
    SQLALCHEMY_MAX_OVERFLOW = 0
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

class AppRun(object):
    host = 'localhost'
    port = 5000
    debug = True
