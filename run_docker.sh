#!/bin/bash
# =============================================================================
# run_docker.sh — One-click Docker setup for AI Resume Analyzer Pro (Linux/Mac)
# =============================================================================

set -e

echo "============================================================"
echo "   AI Resume Analyzer Pro — Docker Setup"
echo "============================================================"
echo ""

# ---- Check Docker ----
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker is not installed."
    echo "Install from: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "[OK] Docker detected."

# ---- Check Docker Compose ----
if ! docker compose version &> /dev/null; then
    echo "[ERROR] Docker Compose is not available."
    exit 1
fi
echo "[OK] Docker Compose detected."
echo ""

# ---- Create .env from example if missing ----
if [ ! -f .env ]; then
    echo "[INFO] Creating .env from .env.example ..."
    cp .env.example .env
    echo "[WARN] .env created with default values."
    echo "[WARN] Please edit .env to set your actual API keys:"
    echo "       - GEMINI_API_KEY"
    echo "       - GOOGLE_OAUTH_CLIENT_ID / SECRET"
    echo "       - FACEBOOK_OAUTH_CLIENT_ID / SECRET"
    echo "       - SECRET_KEY"
    echo ""
    read -p "Press Enter to continue after editing .env (or Ctrl+C to abort)..."
fi

# ---- Build and start ----
echo "[INFO] Building and starting Docker containers..."
echo ""

docker compose up --build -d

echo ""
echo "============================================================"
echo "   SUCCESS! Application is running."
echo "============================================================"
echo ""
echo "   Local URL:      http://localhost:5000"
echo "   PostgreSQL:     localhost:5432"
echo ""
echo "   Useful commands:"
echo "     docker compose logs -f web    (view Flask logs)"
echo "     docker compose ps             (list running services)"
echo "     docker compose down           (stop all services)"
echo ""

