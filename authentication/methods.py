import logging

import hashlib
import secrets

from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database.usersdb import users_database, users

from settings import ADMIN_HASH_USERNAME, ADMIN_HASH_PASSWORD

from utils.security import verify_hash

logger = logging.getLogger(__name__)


def authenticate_admin(request: Request,
                       credentials: HTTPBasicCredentials = Depends(
                           HTTPBasic())) -> str:
    """
    [Method for authenticating admin credentials.]

    Args:
        request (Request): [API request object.]
        credentials (HTTPBasicCredentials, optional): [Admin credentials].
            Defaults to Depends( HTTPBasic()).

    Raises:
        HTTPException: [Unauthorized admin access.]

    Returns:
        str: [Username for admin.]
    """
    IP = request.client.host
    _username = credentials.username
    password = credentials.password
    hashed_username = hashlib.sha256(_username.encode()).hexdigest()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    correct_username = secrets.compare_digest(hashed_username,
                                              ADMIN_HASH_USERNAME)
    correct_password = secrets.compare_digest(hashed_password,
                                              ADMIN_HASH_PASSWORD)
    if not (correct_username and correct_password):
        logger.warning('Failed authentication attempt was made for admin '
                       f'with username {_username} from IP address {IP}.')
        raise HTTPException(status_code=401,
                            detail="You ain't the admin bitch!",
                            headers={"WWW-Authenticate": "Basic"})
    return _username


async def authenticate_user(request: Request,
                            credentials: HTTPBasicCredentials = Depends(
                                HTTPBasic())) -> str:
    """
    [Method for authenticating user credentials.]

    Args:
        request (Request): [API request object.]
        credentials (HTTPBasicCredentials, optional): [User credentials.].
            Defaults to Depends( HTTPBasic()).

    Raises:
        HTTPException: [Incorrect password.]
        HTTPException: [Inactive user.]
        HTTPException: [Unauthorized user.]

    Returns:
        str: [Username for user.]
    """
    IP = request.client.host
    _username = credentials.username
    password = credentials.password
    query = users.select().where(users.c.username == _username)
    user = await users_database.fetch_one(query)
    if user:
        if user['active']:
            user_salt = user['salt']
            user_password = user['password']
            if verify_hash(password + user_salt, user_password):
                return _username
            else:
                logger.warning(
                    'Failed authentication attempt was made with incorrect '
                    f'password for user {_username} with IP address {IP}.'
                )
                raise HTTPException(status_code=401,
                                    detail="Incorrect password.")
        else:
            logger.warning(
                'Failed authentication attempt was made for inactive '
                f'user {_username} with IP address {IP}.'
            )
            raise HTTPException(status_code=401,
                                detail=f"User {_username} is inactive.")
    else:
        logger.warning(
            'Failed authentication attempt was made for unauthorized '
            f'user {_username} with IP address {IP}.'
        )
        raise HTTPException(status_code=401,
                            detail=f"Unauthorized user {_username}.")
