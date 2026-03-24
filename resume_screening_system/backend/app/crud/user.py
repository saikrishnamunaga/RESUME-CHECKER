from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRegister
from app.core.security import get_password_hash, verify_password
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return False
    return user

def create_user(db: Session, user: UserRegister):
    if not user.email.endswith('@gmail.com'):
        raise ValueError("Only Gmail accounts allowed")
    hashed_password = get_password_hash(user.password)
    db_user = User(
        name=user.name,
        email=user.email,
        password_hash=hashed_password,
        login_type='email'
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_usage(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        today = datetime.now().date()
        user.daily_usage += 1
        # Reset monthly if new month
        if user.monthly_usage >= 300:  # Pro max
            user.monthly_usage = 1
        else:
            user.monthly_usage += 1
        db.commit()
    return user

def check_user_quota(db: Session, user: User):
    today = datetime.now().date()
    # Reset daily quota daily
    if user.daily_usage >= 5 and user.plan == 'free':
        return False, "Free quota exceeded (5/day)"
    if user.monthly_usage >= 300 and user.plan == 'pro':
        return False, "Pro quota exceeded (300/month)"
    return True, "OK"

