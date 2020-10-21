import secrets
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "USERNAME")     # Insert own username.
    correct_password = secrets.compare_digest(credentials.password, "PASSWORD")     # Insert own password.
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code =   status.HTTP_401_UNAUTHORIZED,
            detail      =   "Incorrect username or password.",
            headers     =   {"WWW-Authenticate": "Basic"},
        )
    return credentials.username