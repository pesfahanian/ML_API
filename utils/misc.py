import os
import uuid
from datetime import datetime

from .security import make_salt


def store_file(_file, credentials):
    """
    Stores a given file into the data directory.
    """
    data_path = os.getcwd() + '/data/'
    filename = _file.filename.replace(" ", "_")
    user, timestamp, _id = credentials[0], credentials[1], credentials[2]
    file_path = f'{os.getcwd()}/data/{user}/{user}_{timestamp}_{_id}_{filename}'
    directories = [name for name in os.listdir(data_path) if os.path.isdir(os.path.join(data_path, name))]
    if user not in directories:
        os.mkdir(os.path.join(data_path, str(user)))
    execute_store_file(_file, file_path)
    return file_path


def execute_store_file(_file, path):
    """
    Executes the storage for a given file in a given path.
    """
    with open(path, 'wb+') as f:
        f.write(_file.file.read())
        f.close()


def inference_credentials():
    """
    Return a generated inference credentials.
    """
    ID = str(uuid.uuid1())
    now = datetime.now()
    return ID, now


def user_credentials():
    """
    Return a generated user credentials.
    """
    ID = str(uuid.uuid1())
    now = datetime.now()
    salt = make_salt()
    return ID, now, salt
