import databases

import sqlalchemy
from sqlalchemy.types import DateTime
from sqlalchemy_utils import database_exists, create_database

from settings import POSTGRES_DATABASE_USER, POSTGRES_DATABASE_PASSWORD, POSTGRES_DATABASE_URL, POSTGRES_DATABASE_PORT


POSTGRES_DATABASE = f'postgresql://{POSTGRES_DATABASE_USER}:{POSTGRES_DATABASE_PASSWORD}@{POSTGRES_DATABASE_URL}:{POSTGRES_DATABASE_PORT}'

# Postgres inferences database
INFERENCES_DATABASE_NAME = 'ml_inferences'
INFERENCES_DATABASE_URI =  f'{POSTGRES_DATABASE}/{INFERENCES_DATABASE_NAME}'

inferences_database = databases.Database(INFERENCES_DATABASE_URI)
inferences_metadata = sqlalchemy.MetaData()

inferences = sqlalchemy.Table(
    "MLInferences",
    inferences_metadata,
    sqlalchemy.Column("id",             sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("timestamp",      sqlalchemy.DateTime),
    sqlalchemy.Column("ip",             sqlalchemy.String),
    sqlalchemy.Column("user",           sqlalchemy.String),
    sqlalchemy.Column("filename",       sqlalchemy.String),
    sqlalchemy.Column("path",           sqlalchemy.String),
    sqlalchemy.Column("validated",      sqlalchemy.Boolean),
    sqlalchemy.Column("result",         sqlalchemy.JSON),
)

inferences_engine = sqlalchemy.create_engine(INFERENCES_DATABASE_URI)
if not database_exists(inferences_engine.url):
    create_database(inferences_engine.url)
inferences_metadata.create_all(inferences_engine)
