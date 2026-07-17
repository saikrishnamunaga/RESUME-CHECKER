from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
from app.core.config import get_settings
from app.database import engine, Base
from app.api.v1 import api

settings = get_settings()
app = FastAPI(title=settings.PROJECT_NAME)

# DB
Base.metadata.create_all(bind=engine)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_URL.split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"msg": "AI Resume Screening API"}

