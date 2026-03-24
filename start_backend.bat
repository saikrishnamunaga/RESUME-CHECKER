@echo off
echo Starting FastAPI Backend...
cd /d "D:\ml &nlp project\resume_screening_system\backend"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
