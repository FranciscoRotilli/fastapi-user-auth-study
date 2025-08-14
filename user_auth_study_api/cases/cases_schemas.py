from pydantic import BaseModel
from cases_models import CaseStatus
from datetime import datetime
from typing import List

class OwnerResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class CaseBase(BaseModel):
    name: str
    case_number: str

class CaseCreate(CaseBase):
    pass

class CaseResponse(CaseBase):
    id: int
    status: CaseStatus
    created_at: datetime
    updated_at: datetime
    owner: OwnerResponse

    class Config:
        from_attributes = True