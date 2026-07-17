from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import List
from app.core.security import get_current_active_user
import app.crud.user as crud_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.services.storage import validate_and_extract
from app.services.nlp import nlp_engine
from app.schemas.screening import ScreeningResponse
from app.models.screening import Screening
import json

router = APIRouter()

@router.post("/", response_model=List[ScreeningResponse])
async def screen_resumes(
    resumes: List[UploadFile] = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    ok, msg = crud_user.check_user_quota(db, current_user)
    if not ok:
        raise HTTPException(status_code=429, detail=msg)
    
    texts = await validate_and_extract(resumes)
    results = []
    
    for text_data in texts:
        result = nlp_engine.compute_match_score(text_data["text"], job_description)
        if current_user.plan == 'pro':
            result['ats_score'] = 92  # Pro feature
            result['errors'] = ['Minor formatting']
            result['suggestions'] = ['Add LinkedIn']
        else:
            result['ats_score'] = None
            result['errors'] = []
            result['suggestions'] = []
        
        results.append(result)
        
        # Save
        screening = Screening(
            user_id=current_user.id,
            resume_filename=text_data["filename"],
            job_desc=job_description,
            domain=result["domain"],
            score=result["score"],
            results=json.dumps(result)
        )
        db.add(screening)
    
    db.commit()
    crud_user.update_user_usage(db, current_user.id)
    
    return results
