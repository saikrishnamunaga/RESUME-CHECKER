# =============================================================================
# Dockerfile — AI Resume Analyzer Pro (Flask)
# =============================================================================
# Multi-stage build:
#   1)  builder   — install Python dependencies into a virtual environment
#   2)  runtime   — minimal slim image with just the venv + app code
# =============================================================================

# ---- Stage 1: builder ------------------------------------------------------
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install system libraries required by pdfplumber, reportlab, python-docx, etc.
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        build-essential \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching
COPY requirements.txt .

# Additional packages required at runtime but not yet listed in requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        google-genai \
        reportlab

# ---- Stage 2: runtime ------------------------------------------------------
FROM python:3.11-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=5000

WORKDIR /app

# Minimal runtime OS deps (fonts for reportlab PDF generation)
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Copy the virtual environment from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create runtime directories
RUN mkdir -p uploads instance

# Expose the application port
EXPOSE ${PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/')" || exit 1

# Run with gunicorn (production-grade WSGI server)
CMD ["sh", "-c", "gunicorn run:app --bind 0.0.0.0:${PORT} --workers 4 --timeout 120 --access-logfile - --error-logfile -"]

