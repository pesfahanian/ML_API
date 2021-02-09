import databases

import sqlalchemy
from sqlalchemy.types import DateTime
from sqlalchemy_utils import database_exists, create_database

from settings import POSTGRES_DATABASE_USER, POSTGRES_DATABASE_PASSWORD, POSTGRES_DATABASE_URL, POSTGRES_DATABASE_PORT

POSTGRES_DATABASE = f'postgresql://{POSTGRES_DATABASE_USER}:{POSTGRES_DATABASE_PASSWORD}@{POSTGRES_DATABASE_URL}:{POSTGRES_DATABASE_PORT}'

# Postgres users database
USERS_DATABASE_NAME = 'ml_users'
USERS_DATABASE_URI =  f'{POSTGRES_DATABASE}/{USERS_DATABASE_NAME}'

users_database = databases.Database(USERS_DATABASE_URI)
users_metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "MLUsers",
    users_metadata,
    sqlalchemy.Column("id",             sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("registerDate",   sqlalchemy.DateTime),
    sqlalchemy.Column("updateDate",     sqlalchemy.DateTime),
    sqlalchemy.Column("username",       sqlalchemy.String, unique=True),
    sqlalchemy.Column("salt",           sqlalchemy.String), #todo try unique salt later
    sqlalchemy.Column("password",       sqlalchemy.String),
    sqlalchemy.Column("active",         sqlalchemy.Boolean),
)

users_engine = sqlalchemy.create_engine(USERS_DATABASE_URI)
if not database_exists(users_engine.url):
    create_database(users_engine.url)
users_metadata.create_all(users_engine)
