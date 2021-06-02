from celery.result import AsyncResult

from worker.celery import app


def get_result(id: str):
    """
    [Get the result of celery worker.]

    Args:
        id ([str]): [ID of celery task.]

    Returns:
        [type]: [Result of the celery task.]
    """
    r = AsyncResult(id, app=app)
    result = r.get()
    return result
