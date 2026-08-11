#!/bin/sh
# =============================================================================
# docker-entrypoint.sh — Database migration + app startup
# =============================================================================
set -e

echo "→ Running database migrations..."
flask db upgrade || echo "⚠️  Migration failed (maybe first run). Continuing..."

echo "→ Starting AI Resume Analyzer Pro..."
exec "$@"

