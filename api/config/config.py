import os 
from decouple import config
from datetime import timedelta

# config_file_path = "/Users/admin/student/student management API/api/config/config.py"
# config_dir_path = os.path.dirname(config_file_path)

# if not os.access(config_dir_path, os.W_OK):
#     print("Error: The directory '{0}' is not writable.".format(config_dir_path))



BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config('SECRET_KEY', 'secret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(Config):
    DEBUG = config('DEBUG', True, cast=bool)
    SQLALCHEMY_ECHO =True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3')

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'test_db.sqlite3')

class ProdConfig(Config):
    pass

config_dict = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}