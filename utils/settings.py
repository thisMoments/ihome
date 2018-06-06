
import os
from utils.functions import get_database_uri


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STATIC_DIR = os.path.join(BASE_DIR, 'static')

TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')

DATABASE = {
    'db': 'mysql',
    'driver': 'pymysql',
    'host': '47.96.130.236',
    'port': '3306',
    'user': 'root',
    'password': '123456',
    'name': 'ihome'
}

SQLALCHEMY_DATABASE_URI = get_database_uri(DATABASE)

UPLOAD_DIRS = os.path.join(os.path.join(BASE_DIR, 'static'), 'upload')
