from fastapi import Header, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from .security import get_current_active_user
from app.crud import user

async def verify_gmail_only(current_user=Depends(get_current_active_user), db=Depends(get_db)):
    if not current_user.email.endswith("@gmail.com"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Gmail accounts allowed"
        )
    return current_user
