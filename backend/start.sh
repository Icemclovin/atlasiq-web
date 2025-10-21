#!/bin/sh
# Startup script for Railway deployment
set -e

echo "🚀 Starting AtlasIQ Backend..."

# Run database initialization
python docker_init.py

# Start uvicorn with Railway's PORT or default to 8000
PORT=${PORT:-8000}
echo "🌐 Starting server on port $PORT"
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
