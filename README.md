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

