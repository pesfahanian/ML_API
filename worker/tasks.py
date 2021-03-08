from inference.model import predict

from worker.celery import app


@app.task(name = 'model')
def run(path):
    """
    Celery task.
    """
    result = predict(path)
    return result
