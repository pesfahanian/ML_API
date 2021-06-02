import os
import uuid
from typing import Union
from datetime import date, datetime

from utils.security import make_salt


def store_file(_file, credentials: list) -> str:
    """
    [Stores a given file into the data directory.]

    Args:
        _file ([type]): [File to be stored.]
        credentials (list): [Credentials of storage action.]

    Returns:
        str: [Path of stored file.]
    """
    data_path = os.getcwd() + '/data/'
    filename = _file.filename.replace(" ", "_")
    user, timestamp, _id = credentials[0], credentials[1], credentials[2]
    file_path = f'{os.getcwd()}/data/{user}/{user}_{timestamp}_{_id}_{filename}'
    directories = [
        name for name in os.listdir(data_path)
        if os.path.isdir(os.path.join(data_path, name))
    ]
    if user not in directories:
        os.mkdir(os.path.join(data_path, str(user)))
    execute_store_file(_file, file_path)
    return file_path


def execute_store_file(_file, path: str) -> None:
    """
    [Executes the storage for a given file in a given path.]

    Args:
        _file ([type]): [File to be stored.]
        path (str): [Path to store at.]
    """
    with open(path, 'wb+') as f:
        f.write(_file.file.read())
        f.close()


def inference_credentials() -> Union[str, datetime]:
    """
    [Generate inference credentials.]

    Returns:
        Union[str, datetime]: [Inference credentials.]
    """
    ID = str(uuid.uuid1())
    now = datetime.now()
    return ID, now


def user_credentials() -> Union[str, datetime, str]:
    """
    [Generate user credentials.]

    Returns:
        Union[str, datetime, str]: [User credentials.]
    """
    ID = str(uuid.uuid1())
    now = datetime.now()
    salt = make_salt()
    return ID, now, salt
