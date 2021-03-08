import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from API.base import routers as base_routers
from API.records import routers as records_routers
from API.inference import routers as inference_routers
from API.dashboard import routers as dashboard_routers

from database.usersdb import users_database
from database.inferencesdb import inferences_database

from settings import PATH, VERSION
from settings.logger import setup_logging_pre


logger = logging.getLogger('API')
setup_logging_pre()


app = FastAPI(title         =   "ML-API",
              description   =   "API Documentation and endpoint access for running inference using DenseNet.",
              version       =   str(VERSION),
              docs_url      =   None,
              redoc_url     =   None,
              debug         =   False)


@app.on_event("startup")
async def startup():
    """
    Connects to database(s) on app startup.
    """
    await users_database.connect()
    logger.info('Connected to users database.')
    await inferences_database.connect()
    logger.info('Connected to inferences database.')


@app.on_event("shutdown")
async def shutdown():
    """
    Disconnects from database(s) on app shoutdown.
    """
    await users_database.disconnect()
    logger.info('Disconnected from users database.')
    await inferences_database.disconnect()
    logger.info('Disconnected from inferences database.')


@app.get("/", status_code=307)
async def root_redirect():
    """
    Redirects to root.
    """
    response = RedirectResponse(url=PATH+"/root/")
    return response


@app.get("/docs", status_code=307)
async def docs_redirect():
    """
    Redirects to docs.
    """
    response = RedirectResponse(url=PATH+"/docs/")
    return response


app.include_router(base_routers.router)
app.include_router(records_routers.router)
app.include_router(inference_routers.router)
app.include_router(dashboard_routers.router)
