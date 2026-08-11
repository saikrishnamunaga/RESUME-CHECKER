@echo off
:: =============================================================================
:: run_docker.bat — One-click Docker setup for AI Resume Analyzer Pro
:: =============================================================================
:: This script will:
::   1. Check prerequisites (Docker, WSL2)
::   2. Copy .env.example to .env if missing
::   3. Build and start all services
:: =============================================================================

title AI Resume Analyzer Pro — Docker Setup

echo ============================================================
echo    AI Resume Analyzer Pro — Docker Setup
echo ============================================================
echo.

:: ---- Check Docker ----
where docker >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker is not installed.
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)

echo [OK] Docker detected.

:: ---- Check Docker Compose ----
docker compose version >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Docker Compose is not available.
    pause
    exit /b 1
)

echo [OK] Docker Compose detected.
echo.

:: ---- Create .env from example if missing ----
if not exist .env (
    echo [INFO] Creating .env from .env.example ...
    copy .env.example .env >nul
    echo [WARN] .env created with default values.
    echo [WARN] Please edit .env to set your actual API keys:
    echo        - GEMINI_API_KEY
    echo        - GOOGLE_OAUTH_CLIENT_ID / SECRET
    echo        - FACEBOOK_OAUTH_CLIENT_ID / SECRET
    echo        - SECRET_KEY
    echo.
    pause
)

:: ---- Build and start ----
echo [INFO] Building and starting Docker containers...
echo.

docker compose up --build -d

if %ERRORLEVEL% equ 0 (
    echo.
    echo ============================================================
    echo    SUCCESS! Application is running.
    echo ============================================================
    echo.
    echo    Local URL:      http://localhost:5000
    echo    PostgreSQL:     localhost:5432
    echo.
    echo    Useful commands:
    echo      docker compose logs -f web    (view Flask logs)
    echo      docker compose ps             (list running services)
    echo      docker compose down           (stop all services)
    echo.
) else (
    echo [ERROR] Docker Compose failed. Check the output above.
    pause
    exit /b 1
)

pause

