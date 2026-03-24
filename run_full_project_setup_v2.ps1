Write-Host "Starting full project fix & launch..." -ForegroundColor Cyan

# ----------------------------
# Backend Setup
# ----------------------------
Write-Host "`n[Backend] Cleaning old virtual environment..." -ForegroundColor Green
cd .\resume_screening_system\backend

if (Test-Path "venv") {
    Remove-Item -Recurse -Force venv
    Write-Host "Old venv deleted." -ForegroundColor Yellow
}

# Create new venv
Write-Host "Creating new venv..." -ForegroundColor Green
python -m venv venv

# Activate venv and upgrade pip
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip

# Install backend dependencies
Write-Host "Installing backend dependencies..." -ForegroundColor Green
pip install fastapi uvicorn sqlalchemy pydantic "python-jose[cryptography]" "passlib[bcrypt]" bcrypt python-dotenv google-auth google-auth-oauthlib google-auth-httplib2 sentence-transformers spacy scikit-learn PyPDF2 python-multipart email-validator python-dateutil

# Download SpaCy model
python -m spacy download en_core_web_sm

Write-Host "[Backend setup complete]" -ForegroundColor Cyan

# ----------------------------
# Frontend Setup
# ----------------------------
Write-Host "`n[Frontend] Cleaning old node_modules..." -ForegroundColor Green
cd ..\frontend

if (Test-Path "node_modules") {
    Remove-Item -Recurse -Force node_modules
    Write-Host "node_modules deleted." -ForegroundColor Yellow
}

if (Test-Path "package-lock.json") {
    Remove-Item -Force "package-lock.json"
    Write-Host "package-lock.json deleted." -ForegroundColor Yellow
}

# Install frontend dependencies
Write-Host "Installing frontend dependencies..." -ForegroundColor Green
npm install

Write-Host "[Frontend setup complete]" -ForegroundColor Cyan

# ----------------------------
# Launch Servers in Separate Windows
# ----------------------------
Write-Host "`nLaunching backend server..." -ForegroundColor Green
$backendPath = (Get-Location).Path + '\resume_screening_system\backend'
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$backendPath'; .\\venv\\Scripts\\Activate.ps1; uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"

Write-Host "Launching frontend dev server..." -ForegroundColor Green
$frontendPath = $backendPath -replace '\\backend$', '\\frontend'
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$frontendPath'; npm run dev"

Write-Host "`n✅ Both backend and frontend are starting in separate windows!" -ForegroundColor Cyan
Write-Host "Backend: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Green
