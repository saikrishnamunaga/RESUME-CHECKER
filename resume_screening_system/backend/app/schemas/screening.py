from pydantic import BaseModel
from typing import List, Dict

class ScreeningBase(BaseModel):
    pass

class ScreeningCreate(ScreeningBase):
    resumes: List[str]
    job_description: str

class ScreeningResponse(BaseModel):
    domain: str
    score: float
    strengths: List[str]
    missing: List[str]
    suggestions: List[str]

    class Config:
        from_attributes = True

