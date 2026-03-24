from fastapi import APIRouter, Depends, HTTPException, status
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from app.core.config import get_settings
from app.core.security import create_access_token
from app.database import get_db
from app.schemas.user import Token
import app.crud.user as crud_user
from sqlalchemy.orm import Session

router = APIRouter()
settings = get_settings()

@router.post("/google", response_model=Token)
async def google_login(token_data: dict, db: Session = Depends(get_db)):
    try:
        # Verify Google token
        id_info = id_token.verify_oauth2_token(token_data["token"], Request(), settings.GOOGLE_CLIENT_ID)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")
        
        email = id_info['email']
        name = id_info['name']
        
        if not email.endswith("@gmail.com"):
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Gmail accounts only")
        
        user = crud_user.get_user_by_email(db, email)
        if not user:
            user_create = app.schemas.user.UserCreate(name=name, email=email)
            user = crud_user.create_user(db, user_create)
            user.login_type = 'google'
            db.commit()
            db.refresh(user)
        
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}
    
    except ValueError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token")

