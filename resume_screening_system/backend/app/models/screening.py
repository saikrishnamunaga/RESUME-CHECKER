from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from ..database import Base

class Screening(Base):
    __tablename__ = "screenings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_filename = Column(String)
    job_desc = Column(String)
    domain = Column(String)
    score = Column(Float)
    results = Column(String)  # JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now())

