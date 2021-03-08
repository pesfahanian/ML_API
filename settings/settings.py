import os
from configparser import ConfigParser


VERSION = 2
V = 'v' + str(VERSION)
PATH = "/api/" + V


CREDENTIALS_PATH = f'{os.getcwd()}/settings/credentials.cfg'
config_object = ConfigParser()
config_object.read(CREDENTIALS_PATH)


DEVELOP_MODE_ENV = os.environ.get('DEVELOP_MODE', True)
if DEVELOP_MODE_ENV == 'false':
    DEVELOP_MODE = False
else:
    DEVELOP_MODE = True


ACCEPTABLE_FILE_SUFFIXES = os.environ.get('ACCEPTABLE_FILE_SUFFIXES', ['jpg', 'jpeg', 'png'])
ACCEPTABLE_FILE_FORMATS = os.environ.get('ACCEPTABLE_FILE_FORMATS', ['image/jpeg', 'image/png'])


# Security variables
SALT_LENGTH = os.environ.get('SALT_LENGTH', 16)
if DEVELOP_MODE:
    ADMIN_HASH_USERNAME = config_object['Security']['ADMIN_HASH_USERNAME']
    ADMIN_HASH_PASSWORD = config_object['Security']['ADMIN_HASH_PASSWORD']
else:
    ADMIN_HASH_USERNAME = os.environ.get('ADMIN_HASH_USERNAME', None)
    ADMIN_HASH_PASSWORD = os.environ.get('ADMIN_HASH_PASSWORD', None)


# Databases variables
POSTGRES_DATABASE_USER = os.environ.get('POSTGRES_USER', 'postgres')
if DEVELOP_MODE:
    POSTGRES_DATABASE_PASSWORD = config_object['Database']['POSTGRES_DATABASE_PASSWORD']
else:
    POSTGRES_DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', None)
POSTGRES_DATABASE_URL = os.environ.get('POSTGRES_DATABASE_URL', 'localhost')
POSTGRES_DATABASE_PORT = os.environ.get('POSTGRES_DATABASE_PORT', 5432)


# Redis variables
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', '')
REDIS_HOST_ENV = os.environ.get('REDIS_HOST', '')
if REDIS_PASSWORD:
    if not REDIS_HOST_ENV:
        REDIS_HOST = f'redis://:{REDIS_PASSWORD}@localhost:6379/0'
    else:
        REDIS_HOST = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST_ENV.split('redis://')[1]}"
else:
    REDIS_HOST = os.environ.get('REDIS_HOST', 'redis://localhost:6379/')
