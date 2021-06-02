from inference.model import predict

from worker.celery import app


@app.task(name='model')
def run(path: str):
    """
    [Celery task to run inference.]

    Args:
        path ([str]): [Path of image file to be inferred.]

    Returns:
        [type]: [Inference result.]
    """
    result = predict(path)
    return result
