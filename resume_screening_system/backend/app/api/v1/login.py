from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserLogin, Token
from app.crud.user import authenticate_user
from app.core.security import create_access_token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, email=form_data.email, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
