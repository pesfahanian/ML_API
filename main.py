import uuid
import datetime
from sqlalchemy.orm.exc import NoResultFound
from typing import List
from fastapi import FastAPI, Depends, HTTPException

from ml import DX_Chest
from ml import prep, predict
from save import save_img
from database import database, cases
from schema import CaseList, CaseEntry
from authentication import authenticate

modalities = ['DX_Chest']

print('------------------------------------------------------------------')

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get('/')
async def index(username: str = Depends(authenticate)):
    return "Machine Learning API with basic authentication implemented with FastAPI and PostgreSQL."

@app.get("/cases", response_model=List[CaseList])
async def get_all_cases(username: str = Depends(authenticate)):
    query = cases.select()
    return await database.fetch_all(query)
    
@app.get("/cases/{caseID}", response_model=CaseList)
async def get_case_by_id(caseID: str, username: str = Depends(authenticate)):
    query = cases.select().where(cases.c.id == caseID)
    result = await database.fetch_one(query)
    if (result != None):    # Error handling for when record is not found.
        return result 
    else:
        raise HTTPException(status_code=404, detail="Case not found.")

@app.post("/cases", response_model=CaseList)
async def register_case(case: CaseEntry, username: str = Depends(authenticate)):
    if (case.modality in modalities):
        if (case.modality == 'DX_Chest'):
            model = DX_Chest
        ID = str(uuid.uuid1())
        now = str(datetime.datetime.now()).replace(' ', '-').split('.')[0]
        case_path = save_img(case.patient, case.url, now)
        diagnosis = predict(case_path, model)
        query = cases.insert().values(
            id          =   ID,
            date        =   now,
            patient     =   case.patient,
            url         =   case.url,
            modality    =   case.modality,
            diagnosis   =   diagnosis
        )
        await database.execute(query)
        return {
            **case.dict(),
            "id":           ID,
            "date":         now,
            "diagnosis":    diagnosis
        }
    else:
        raise HTTPException(status_code=420, detail="Requested modelity not supported.")
    
@app.delete("/cases/{caseID}")
async def delete_case(caseID: str, username: str = Depends(authenticate)):
    exist = cases.select().where(cases.c.id == caseID)
    result = await database.fetch_one(exist)
    if (result != None):    # Error handling for when record is not found.
        query = cases.delete().where(cases.c.id == caseID)
        await database.execute(query)
        return {
            "id":       caseID,
            "message":  "Case deleted."
        }
    else:
        raise HTTPException(status_code=404, detail="Case not found.")