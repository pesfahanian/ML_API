import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException

from .urls import DASHBOARD_ENDPOINT

from authentication.decorator import authentication

from database.usersdb import users_database, users

from utils.security import make_hash
from utils.misc import user_credentials

logger = logging.getLogger(__name__)

router = APIRouter(prefix=DASHBOARD_ENDPOINT,
                   tags=["Dashboard"],
                   responses={404: {
                       "description": "Not found"
                   }})


@router.get("/query/", status_code=200)
@authentication.admin_required
async def query_all_users():
    """
    [Query all user records in the users database.]
    """
    logger.info('Querying all user records.')
    query = users.select()
    return await users_database.fetch_all(query)


@router.post("/query/", status_code=200)
@authentication.admin_required
async def query_user(username: str):
    """
    [Query one user record in the users database.]

    Args:
        username (str): [Username of user to be queried.]

    Raises:
        HTTPException: [User does not exist.]

    Returns:
        [type]: [User record.]
    """
    logger.info(f'Querying record for user {username}.')
    query = users.select().where(users.c.username == username)
    result = await users_database.fetch_one(query)
    if result:
        logger.info(f'Record found for user {username}.')
        return result
    else:
        logger.warning(f'User {username} does not exist.')
        raise HTTPException(status_code=404,
                            detail=f"User {username} does not exist.")


@router.post("/register/", status_code=200)
@authentication.admin_required
async def register_user(username: str, password: str, passwordConfirm: str):
    """
    [Register a new user by adding one record to the users database.]

    Args:
        username (str): [Username of user.]
        password (str): [Password of user.]
        passwordConfirm (str): [Password confirmation.]

    Raises:
        HTTPException: [User already exists.]
        HTTPException: [Passwords do not match.]

    Returns:
        [type]: [Record of registered user.]
    """
    logger.info(f'Registering user {username}.')
    if (password == passwordConfirm):
        ID, now, salt = user_credentials()
        hash_pasword = make_hash(password + salt)
        query = users.insert().values(id=ID,
                                      registerDate=now,
                                      updateDate=now,
                                      username=username,
                                      salt=salt,
                                      password=hash_pasword,
                                      active=True)
        try:
            await users_database.execute(query)
            logger.info(f'User {username} created at {now} with ID {ID}.')
        except Exception:
            logger.warning(f'User {username} already exists.')
            raise HTTPException(status_code=409,
                                detail=f"User {username} already exists.")
        response = {
            "id": ID,
            "registerDate": now,
            "username": username,
            "active": True
        }
        return response
    else:
        raise HTTPException(status_code=400,
                            detail="Password confirmation doesn't match.")


@router.patch("/change/", status_code=200)
@authentication.admin_required
async def change_password(username: str, password: str, passwordConfirm: str):
    """
    [Change an existing user's password by updating
        the user's record in the users database.]

    Args:
        username (str): [Username of user.]
        password (str): [New password.]
        passwordConfirm (str): [Password confirmation.]

    Raises:
        HTTPException: [User already exists.]
        HTTPException: [Passwords do not match.]

    Returns:
        [type]: [Confirmation message.]
    """
    logger.info(f'Changing password for user {username}.')
    if (password == passwordConfirm):
        exist = users.select().where(users.c.username == username)
        exist_result = await users_database.fetch_one(exist)
        if exist_result:
            salt = exist_result['salt']
            new_password = make_hash(password + salt)
            now = datetime.now()
            query = users.update().values(
                updateDate=now,
                password=new_password).where(users.c.username == username)
            await users_database.execute(query)
            logger.info(f'Password changed for user {username} at {now}.')
            return {
                "Message": f'Password changed for user {username} at {now}.'
            }
        else:
            logger.warning(f'User {username} does not exist.')
            raise HTTPException(status_code=404,
                                detail=f"User {username} does not exist.")
    else:
        logger.warning('Password confirmation does not match.')
        raise HTTPException(status_code=400,
                            detail="Password confirmation does not match.")


@router.patch("/activate/", status_code=200)
@authentication.admin_required
async def activate_user(username: str):
    """
    [Set the active status of an existing user to 'True' in the users database.]

    Args:
        username (str): [Username of user.]

    Raises:
        HTTPException: [User does not exist.]

    Returns:
        [type]: [Confirmation message.]
    """
    exist = users.select().where(users.c.username == username)
    exist_result = await users_database.fetch_one(exist)
    if exist_result:
        now = datetime.now()
        query = users.update().values(
            updateDate=now, active=True).where(users.c.username == username)
        await users_database.execute(query)
        logger.info(f'User {username} activated at {now}.')
        return {"Message": f'User {username} activated at {now}.'}
    else:
        logger.warning(f'User {username} does not exist.')
        raise HTTPException(status_code=404,
                            detail=f"User {username} does not exist.")


@router.patch("/deactivate/", status_code=200)
@authentication.admin_required
async def deactivate_user(username: str):
    """
    [Set the active status of an existing user to 'False' in the users database.]

    Args:
        username (str): [Username of user.]

    Raises:
        HTTPException: [User does not exist.]

    Returns:
        [type]: [Confirmation message.]
    """
    exist = users.select().where(users.c.username == username)
    exist_result = await users_database.fetch_one(exist)
    if exist_result:
        now = datetime.now()
        query = users.update().values(
            updateDate=now, active=False).where(users.c.username == username)
        await users_database.execute(query)
        logger.info(f'User {username} deactivated at {now}.')
        return {"Message": f'User {username} deactivated at {now}.'}
    else:
        logger.warning(f'User {username} does not exist.')
        raise HTTPException(status_code=404,
                            detail=f"User {username} does not exist.")


@router.delete("/delete/", status_code=200)
@authentication.admin_required
async def delete_user(username: str):
    """
    [Delete an existing user by removing its record from the users database.]

    Args:
        username (str): [Username of user.]

    Raises:
        HTTPException: [User does not exist.]

    Returns:
        [type]: [Confirmation message.]
    """
    exist = users.select().where(users.c.username == username)
    exist_result = await users_database.fetch_one(exist)
    if exist_result:
        query = users.delete().where(users.c.username == username)
        await users_database.execute(query)
        now = datetime.now()
        logger.info(f'User {username} deleted at {now}.')
        return {"Message": f'User {username} deleted at {now}.'}
    else:
        logger.warning(f'User {username} does not exist.')
        raise HTTPException(status_code=404,
                            detail=f"User {username} does not exist.")
