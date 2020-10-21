# ML_API  

Machine Learning API with basic authentication implemented with [Keras](https://keras.io/), [FastAPI](https://fastapi.tiangolo.com/), and [PostgreSQL](https://www.postgresql.org/).

----------------------------------------
## Usage
Install the requirements:
```sh
pip install requirements.txt
```
Create a new Postgres database named `ML_API_Database` in PgAdmin 4. Configure the username and password in the `database.py` file.  
Configure authentication username and password in the `authentication.py` file.  
Run via the command:
```sh
uvicorn main:app --reload
```
