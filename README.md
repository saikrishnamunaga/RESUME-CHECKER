# 🚀 AI Resume Analyzer Pro

AI Resume Analyzer Pro is a production-ready **Flask** web application that analyzes resumes, calculates ATS scores, rewrites resumes using **Google Gemini AI**, and matches candidates to job descriptions.

---

## ✨ Features

- ✅ User registration & authentication (email + Google + Facebook OAuth)
- ✅ Resume upload (PDF/DOCX) with text extraction
- ✅ ATS scoring & job-description matching
- ✅ Gemini AI-powered resume rewriting
- ✅ Before/after comparison with ATS score improvements
- ✅ Export optimized resume as **DOCX** or **PDF**
- ✅ Dashboard, profile, admin panel, reports history
- ✅ **Docker support** (Flask + PostgreSQL)

---

## 🛠 Tech Stack

| Layer      | Technology                                                          |
|------------|---------------------------------------------------------------------|
| Backend    | Python, Flask 2.2, SQLAlchemy, Flask-Login, Flask-Dance             |
| AI         | Google Gemini 1.5 Pro (`google-genai`)                              |
| Database   | SQLite (dev), PostgreSQL (Docker/prod)                              |
| Frontend   | Bootstrap 5, Font Awesome 6, Vanilla JS                             |
| DevOps     | Docker, Docker Compose, Gunicorn, Nginx                             |

---

## 🐳 Docker Setup (Recommended)

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (Windows/Mac) or Docker Engine (Linux)

### Quick Start

**Windows:**
```bash
run_docker.bat
```

**Linux / Mac:**
```bash
chmod +x run_docker.sh
./run_docker.sh
```

### Manual Docker Steps

```bash
# 1. Copy environment config
cp .env.example .env

# 2. Edit .env with your API keys (GEMINI_API_KEY, OAuth credentials, etc.)

# 3. Build and run
docker compose up --build -d

# 4. Open in browser
#    http://localhost:5000
```

### Docker Services

| Service       | URL                     | Description              |
|---------------|-------------------------|--------------------------|
| Flask App     | http://localhost:5000    | Main application         |
| PostgreSQL    | localhost:5432           | Database                 |

### Useful Docker Commands

```bash
# View logs
docker compose logs -f web

# List services
docker compose ps

# Stop all services
docker compose down

# Rebuild after code changes
docker compose up --build -d

# Production mode
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## 🖥️ Local Development (without Docker)

### 1. Create virtual environment
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
pip install google-genai reportlab
```

### 3. Setup environment
```bash
copy .env.example .env      # Windows
cp .env.example .env        # Mac/Linux
```

Edit `.env` and set at minimum:
```
SECRET_KEY="your-secret-key"
GEMINI_API_KEY="your-gemini-api-key"
```

### 4. Run the app
```bash
python run.py
```

Open: **http://localhost:5000**

### Test Credentials
- **Email:** `test@gmail.com`
- **Password:** `Password123!`

---

## 🔑 Environment Variables

| Variable                     | Required | Description                  |
|------------------------------|----------|------------------------------|
| `SECRET_KEY`                 | ✅ Yes   | Flask session encryption key |
| `GEMINI_API_KEY`             | ✅ Yes   | Google Gemini AI API key     |
| `GOOGLE_OAUTH_CLIENT_ID`     | Optional | Google OAuth login           |
| `GOOGLE_OAUTH_CLIENT_SECRET` | Optional | Google OAuth login           |
| `FACEBOOK_OAUTH_CLIENT_ID`   | Optional | Facebook OAuth login         |
| `FACEBOOK_OAUTH_CLIENT_SECRET` | Optional | Facebook OAuth login         |
| `DATABASE_URL`               | Optional | PostgreSQL connection string |

---

## 📂 Project Structure

```
├── app/
│   ├── __init__.py              # App factory
│   ├── extensions.py            # Flask extensions (DB, login, CSRF)
│   ├── models.py                # SQLAlchemy models
│   ├── forms.py                 # WTForms
│   ├── services/
│   │   ├── gemini_service.py    # Gemini AI integration
│   │   └── resume_service.py    # Resume parsing, scoring, export
│   ├── blueprints/
│   │   ├── main/                # Public pages
│   │   ├── auth/                # Authentication
│   │   ├── dashboard/           # Dashboard (upload, edit, accept)
│   │   └── admin/               # Admin panel
│   └── utils/
│       └── file_utils.py        # File upload helpers
├── templates/                   # Jinja2 templates
├── static/                      # CSS, JS, images
├── uploads/                     # Uploaded resumes (Docker volume)
├── Dockerfile                   # Multi-stage Docker build
├── docker-compose.yml           # Docker compose (Flask + PostgreSQL)
├── docker-compose.prod.yml      # Production overrides
├── docker-entrypoint.sh         # Entrypoint script
├── nginx.conf                   # Nginx config (optional)
├── .env.example                 # Environment template
├── .dockerignore                # Docker ignore rules
├── run_docker.bat               # One-click Docker setup (Windows)
├── run_docker.sh                # One-click Docker setup (Linux/Mac)
├── run.py                       # Entry point
└── config.py                    # Configuration
```

---

## 🧪 Testing

```bash
pytest tests/ -v
```

---

## 🚢 Deployment

### Docker (recommended)
```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Traditional Server
```bash
gunicorn run:app --bind 0.0.0.0:5000 --workers 4
```

---

## 📄 License

MIT — Free for personal and commercial use.

