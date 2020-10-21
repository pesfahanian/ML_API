from pydantic import BaseModel, Field

class CaseList(BaseModel):
    id:         str
    date:       str
    patient:    str
    url:        str
    modality:   str
    diagnosis:  str

class CaseEntry(BaseModel):
    patient:    str = Field(..., example = "Patient Name")
    url:        str = Field(..., example = "https://facebook.com/stipid_image.jpg")
    modality:   str = Field(..., example = "DX_Chest")