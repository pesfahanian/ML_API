from celery.result import AsyncResult

from worker.celery import app

def get_result(id):
    r = AsyncResult(id, app=app)
    result = r.get()
    return result
