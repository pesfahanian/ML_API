from core.model import predict

from worker.celery import app

@app.task(name = 'model')
def run(path):
    result = predict(path)
    return result
