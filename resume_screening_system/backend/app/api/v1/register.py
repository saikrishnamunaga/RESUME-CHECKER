from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserRegister, Token
from app.crud.user import create_user
from app.core.security import create_access_token
from app.core.config import get_settings

router = APIRouter()
settings = get_settings()

@router.post("/register", response_model=Token)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        db_user = create_user(db, user)
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
