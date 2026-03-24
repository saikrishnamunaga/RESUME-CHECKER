# Universal AI Resume Screening System

## Overview
AI-powered system for matching resumes to any job description using BERT embeddings, spaCy NER, domain detection. Full-stack: FastAPI + React.

## Quick Start
```bash
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
```

## Docker
```bash
docker-compose up -d
```

## Features
- Dynamic matching (no fixed skills)
- Google OAuth (@gmail.com only)
- Free/Pro plans
- PDF/DOCX upload (2MB limit)
- Multi-resume ranking

## Tech
- Backend: FastAPI, SentenceTransformers, spaCy
- Frontend: React, Tailwind, Vite
- DB: SQLite (dev), Postgres (prod)

See TODO.md for progress.

