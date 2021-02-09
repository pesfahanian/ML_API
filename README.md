# ML_API

REST API for running inference using
[DenseNet](https://arxiv.org/abs/1608.06993).

Made with
[FastAPI](https://fastapi.tiangolo.com/),
[PostgreSQL](https://www.postgresql.org/),
[Redis](https://redis.io/),
and
[PyTorch](https://pytorch.org/).

Functionalities:
- Admin authentication for swagger documentation and endpoint access.
- Fast and accurate inference on uploaded images using a pre-trained `DenseNet` model.
- User authentication for running inference.
- File validation on upload.
- User-separated storage of uploaded files.
- Full C.R.U.D. on user records database.
- Full C.R.U.D. on inference records database.
- Logger service.

----------------------------------------
## Usage
Clone the repository and relocate to its directory using:
```sh
$ git clone https://github.com/pesfahanian/ML_API.git
$ cd ML_API
```
Install the requirements:
```sh
$ pip install requirements.txt
```
Make sure you have `PostgreSQL` and `Redis` installed.

Run the inference worker using:
```sh
$ celery -A worker.celery worker -l info
```
Start the application with:
```sh
$ uvicorn main:app --host 127.0.0.1 --port 8000
```