Write-Host "Starting full project setup..." -ForegroundColor Cyan

# ----------------------------
# Step 1: Fix Backend (Python)
# ----------------------------
Write-Host "`n[Backend] Cleaning old virtual environment..." -ForegroundColor Green
$backendPath = 'd:/ml &nlp project/resume_screening_system/backend'
cd $backendPath

if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv
    Write-Host "Old venv deleted." -ForegroundColor Yellow
}

# Create new virtual environment
Write-Host "Creating new venv..." -ForegroundColor Green
python -m venv venv

# Activate venv
Write-Host "Activating venv..." -ForegroundColor Green
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Green
python -m pip install --upgrade pip

# Install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Green
pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]" "passlib[bcrypt]" bcrypt python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 sentence-transformers spacy scikit-learn PyPDF2 python-multipart email-validator python-dateutil

# Download SpaCy model
Write-Host "Downloading SpaCy en_core_web_sm model..." -ForegroundColor Green
python -m spacy download en_core_web_sm

Write-Host "[Backend setup complete]" -ForegroundColor Cyan

# ----------------------------
# Step 2: Fix Frontend (Node.js/Vite)
# ----------------------------
Write-Host "`n[Frontend] Cleaning old node_modules..." -ForegroundColor Green
$frontendPath = 'd:/ml &nlp project/resume_screening_system/frontend'
cd $frontendPath

if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force node_modules
    Write-Host "node_modules deleted." -ForegroundColor Yellow
}

if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
    Write-Host "package-lock.json deleted." -ForegroundColor Yellow
}

# Reinstall dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Green
npm install

# Start frontend dev server
Write-Host "Starting Vite dev server..." -ForegroundColor Green
Start-Process "npm" -ArgumentList "run", "dev" -WorkingDirectory $frontendPath

# ----------------------------
# Step 3: Start Backend Server
# ----------------------------
Write-Host "`nStarting FastAPI backend server..." -ForegroundColor Green
Start-Process "python" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" -WorkingDirectory $backendPath

Write-Host "`n✅ Full project setup complete!" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor Green
Read-Host "Press Enter to keep window open"
