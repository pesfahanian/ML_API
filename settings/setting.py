import os

VERSION = 1
V = 'v' + str(VERSION)
PATH = "/api/" + V

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
    ADMIN_HASH_USERNAME = os.environ.get('ADMIN_HASH_USERNAME', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918')
    ADMIN_HASH_PASSWORD = os.environ.get('ADMIN_HASH_PASSWORD', 'ca9911c2e5a3c2a32613689380063c985d7d7084ba63f6d15de5b5dd21d31f65')
else:
    ADMIN_HASH_USERNAME = os.environ.get('ADMIN_HASH_USERNAME', None)
    ADMIN_HASH_PASSWORD = os.environ.get('ADMIN_HASH_PASSWORD', None)

# Databases variables
POSTGRES_DATABASE_USER = os.environ.get('POSTGRES_USER', 'postgres')
if DEVELOP_MODE:
    POSTGRES_DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 1234)
else:
    POSTGRES_DATABASE_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 123456789)
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
