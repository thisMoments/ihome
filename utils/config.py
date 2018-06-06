
import redis

from utils.settings import SQLALCHEMY_DATABASE_URI


class Config:

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # session配置
    SECRET_KEY = 'secret_key'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = redis.Redis(host='localhost', port='6379')
    SESSION_KEY_PREFIX = 's_aj_'



