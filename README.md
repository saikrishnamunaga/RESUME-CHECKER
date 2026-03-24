🚀 Universal AI Resume Screening System

Developed by Munaga Sai Krishna
🔗 GitHub:  https://github.com/saikrishnamunaga/RESUME-CHECKER.gitm
 (replace with your actual link)

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
