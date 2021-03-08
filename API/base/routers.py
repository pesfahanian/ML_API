from fastapi import APIRouter
from fastapi.openapi.docs import get_swagger_ui_html

from authentication.decorator import authentication

from .urls import BASE_ENDPOINT


router = APIRouter(prefix       =   BASE_ENDPOINT,
                   tags         =   ["Base"],
                   responses    =   {404: {"description": "Not found"}})


@router.get("/root/", status_code=200)
@authentication.admin_required
async def root():
    """
    Root path for the API.
    """
    return "Welcome to the ImageNet prediction API."


@router.get("/docs/", status_code=200)
@authentication.admin_required
async def docs():
    """
    Documentation for the API.
    """
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
