from typing import Generator
from fastapi import Depends
from ..database import get_db
from ..core.dependencies import verify_gmail_only
from ..core.security import get_current_user

def get_db_dep(db=Depends(get_db)):
    return db

