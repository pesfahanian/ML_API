import copy
import logging

from fastapi import UploadFile, File
from fastapi import APIRouter, HTTPException, Request

from .urls import INFERENCE_ENDPOINT

from authentication.decorator import authentication

from database.inferencesdb import inferences_database, inferences

from utils.misc import inference_credentials, store_file
from utils.validate import validate_uploaded_file

from worker.tasks import run
from worker.results import get_result


logger = logging.getLogger(__name__)


router = APIRouter(prefix       =   INFERENCE_ENDPOINT,
                   tags         =   ["Inference"],
                   responses    =   {404: {"description": "Not found"}})


@router.post("/upload/", status_code=200)
@authentication.user_required
async def upload(request: Request, _file: UploadFile = File(...)):
    """
    Run inference on an uploaded image.

    This file will be automatically validated to make sure it's a real image file.
    
    **Warning: The image file has to be a real image file with a '.jpg', '.jpeg', or '.png' suffix.**

    - **_file**:     image file
    """
    _temp = copy.deepcopy(_file)
    ID, now = inference_credentials()
    IP = request.client.host
    user = authentication.user
    file_name = _file.filename

    query = inferences.insert().values(
        id          =   ID,
        timestamp   =   now,
        ip          =   IP,
        user        =   user,
        filename    =   file_name,
        path        =   '',
        validated   =   False,
        result      =   {}
    )
    details = (f'database record for '
               f'file with ID {ID} '
               f'for user {user} '
               f'with IP {IP} '
               f'at {now}.')
    try:
        await inferences_database.execute(query)
        logger.info(f'Initiated {details}')
    except Exception as e:
        logger.warning(f'Database error. Reason: {str(e)}')
        detail = {
            "Description": 'Database error',
            "Reason": str(e)
        }
        raise HTTPException(status_code=500, detail=detail)
    
    if validate_uploaded_file(_temp):
        
        stored_path = store_file(_file, [user, now, ID])
        description = (f'inference on file with ID {ID} '
                       f'at path {stored_path} '
                       f'for user {user} '
                       f'with IP {IP} '
                       f'at {now}.')

        try:
            logger.info(f'Running {description}')
            request = run.delay(stored_path)
            task_id = request.id
            result = get_result(task_id)
            logger.info(f'Successful {description}')
        except Exception as e:
            logger.warning(f'Failed {description}')
            logger.warning(f'Failure reason: {str(e)}')
            detail = {
                "Description": 'Model error',
                "Reason": str(e)
            }
            raise HTTPException(status_code=500, detail=detail)
        
        prediction, probability = result[0], result[1]
        logger.info(f'Inference results on file with ID {ID}: '
                    f'Prediction = {prediction} '
                    f'Probability = {probability}.')
        
        query = inferences.update().values(
            path        =   stored_path,
            validated   =   True,
            result      =   {"prediction":  prediction,
                             "probability": probability}
            ).where(inferences.c.id == ID)
        try:
            await inferences_database.execute(query)
            logger.info(f'Updated {details}')
        except Exception as e:
            logger.warning(f'Database error. Reason: {str(e)}')
            detail = {
                "Description": 'Database error',
                "Reason": str(e)
            }
            raise HTTPException(status_code=500, detail=detail)
        
        response = {
            "id":           ID,
            "timestamp":    now,
            "ip":           IP,
            "user":         user,
            "filename":     file_name,
            "validated":    True,
            "result":       {"prediction":   prediction,
                             "probability":  probability}
        }
        return response
