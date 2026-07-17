<<<<<<< HEAD
# AI Resume Analyzer Pro

AI Resume Analyzer Pro is a production-ready Flask web application that analyzes resumes, calculates ATS scores, and matches candidates to job descriptions.

Features
- User registration and authentication
- Resume upload (PDF/DOCX) and parsing
- ATS scoring and job-matching
- Dashboard, profile, and admin panel
- Reports history and PDF export

Tech Stack
- Python, Flask, SQLAlchemy, Flask-Login, Flask-WTF
- SQLite (development), ready to migrate to MySQL/Postgres
- Frontend: Bootstrap 5, Chart.js, Font Awesome

See `config.py` for configuration and `run.py` to start the app.

## Running locally

### Create and activate a virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the app
```bash
python run.py
```

Then open:
- http://localhost:5000

### Environment variables
Set secrets and OAuth credentials via your shell / environment. For example:
- `SECRET_KEY`
- `GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`
- `FACEBOOK_OAUTH_CLIENT_ID`, `FACEBOOK_OAUTH_CLIENT_SECRET`

Uploads and the SQLite DB are stored in the local `uploads/` folder and `ai_resume_analyzer.db` file in the project root.

=======
🚀 Universal AI Resume Screening System

Developed by Munaga Sai Krishna
🔗 GitHub:  https://github.com/saikrishnamunaga/RESUME-CHECKER.gitm
 

Overview

AI-powered system for matching resumes to any job description using BERT embeddings, spaCy NER, and domain detection. Built as a full-stack application using FastAPI and React.

Quick Start
cd resume_screening_system
# Backend
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env
# Edit .env with GOOGLE_CLIENT_ID, etc.
uvicorn backend.app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
Docker
docker-compose up -d
Features
Dynamic matching (no fixed skills)
Google OAuth (@gmail.com only)
Free/Pro plans
PDF/DOCX upload (2MB limit)
Multi-resume ranking
Tech Stack
Backend: FastAPI, SentenceTransformers, spaCy
Frontend: React, Tailwind, Vite
Database: SQLite (dev), PostgreSQL (prod)
>>>>>>> 55722a6e8db69adfff26f81b769ded8a632e0839
