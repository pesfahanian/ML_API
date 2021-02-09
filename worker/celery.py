from celery import Celery

from settings import REDIS_HOST

BROKER_URL  = REDIS_HOST.rstrip('/') + '/0'
BACKEND_URL = REDIS_HOST.rstrip('/') + '/1'

app = Celery(
    'model',
    broker  = BROKER_URL,
    backend = BACKEND_URL,
    include = ['worker.tasks']
    )
