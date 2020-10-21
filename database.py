import databases, sqlalchemy

# Postgres Database
DATABASE_URL = "postgresql://USERNAME:PASSWORD@127.0.0.1:5432/ML_API_Database"      # Insert own username and password.
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

cases = sqlalchemy.Table(
    "Cases",
    metadata,
    sqlalchemy.Column("id",         sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("date",       sqlalchemy.String),
    sqlalchemy.Column("patient",    sqlalchemy.String),
    sqlalchemy.Column("url",        sqlalchemy.String),
    sqlalchemy.Column("modality",   sqlalchemy.String),
    sqlalchemy.Column("diagnosis",  sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)