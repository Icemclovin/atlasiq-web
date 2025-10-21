# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.prod.txt .
RUN pip install --no-cache-dir -r requirements.prod.txt

# Copy application code
COPY . .

# Create directory for SQLite database
RUN mkdir -p /app/data

# Expose port
EXPOSE 8000

# Health check will use Railway's PORT
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; import os; urllib.request.urlopen(f'http://localhost:{os.getenv(\"PORT\", \"8000\")}/health')" || exit 1

# Run initialization and start server
# Print everything for debugging
CMD python docker_init.py && echo "=== DOCKER_INIT COMPLETED ===" && echo "=== STARTING UVICORN ===" && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
