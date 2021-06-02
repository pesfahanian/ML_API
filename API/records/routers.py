import logging

from fastapi import APIRouter, HTTPException

from .urls import RECORDS_ENDPOINT

from authentication.decorator import authentication

from database.inferencesdb import inferences_database, inferences

logger = logging.getLogger(__name__)

router = APIRouter(prefix=RECORDS_ENDPOINT,
                   tags=["Records"],
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/query/", status_code=200)
@authentication.admin_required
async def query_all_inferences():
    """
    [Query all inference records in the inferences database.]
    """
    query = inferences.select()
    logger.info('Querying all inference records.')
    return await inferences_database.fetch_all(query)


@router.post("/query/id/", status_code=200)
@authentication.admin_required
async def query_inference(ID: str):
    """
    [Query one inference record in the inferences database by ID.]

    Args:
        ID (str): [Inference ID.]

    Raises:
        HTTPException: [Inference does not exist.]

    Returns:
        [type]: [Inference record.]
    """
    query = inferences.select().where(inferences.c.id == ID)
    result = await inferences_database.fetch_one(query)
    if result:
        logger.info(f'Querying inference record with {ID}.')
        return result
    else:
        logger.warning(f'Inference record with ID {ID} does not exist.')
        raise HTTPException(
            status_code=404,
            detail=f"Inference record with ID {ID} does not exist.")


@router.post("/query/user/", status_code=200)
@authentication.admin_required
async def query_user_inferences(user: str):
    """
    [Query all inference records in the inferences database for a user.]

    Args:
        user (str): [User.]

    Raises:
        HTTPException: [User does not exist.]

    Returns:
        [type]: [All inference records of user.]
    """
    query = inferences.select().where(inferences.c.user == user)
    result = await inferences_database.fetch_all(query)
    if result:
        logger.info(f'Querying all inference records for user {user}.')
        return result
    else:
        logger.warning(f'User {user} does not exist.')
        raise HTTPException(status_code=404,
                            detail=f"User {user} does not exist.")


@router.delete("/delete/", status_code=200)
@authentication.admin_required
async def delete_inference(ID: str):
    """
    [Delete an inference record from the inferences database.]

    Args:
        ID (str): [Inference ID.]

    Raises:
        HTTPException: [Inference does not exist.]

    Returns:
        [type]: [Success message.]
    """
    exist = inferences.select().where(inferences.c.id == ID)
    exist_result = await inferences_database.fetch_one(exist)
    if exist_result:
        query = inferences.delete().where(inferences.c.id == ID)
        await inferences_database.execute(query)
        logger.info(f'Inference record with ID {ID} deleted!')
        return {"Message": f'Inference record with ID {ID} deleted!'}
    else:
        logger.warning(f'Inference record with ID {ID} does not exist.')
        raise HTTPException(
            status_code=404,
            detail=f"Inference record with ID {ID} does not exist.")
