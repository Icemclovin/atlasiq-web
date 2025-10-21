#!/bin/sh
# Simple test script to debug Railway deployment
echo "=== Debug Info ==="
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "PORT environment: ${PORT:-not set}"
echo "Files in /app:"
ls -la /app
echo ""
echo "Files in /app/app:"
ls -la /app/app
echo ""
echo "=== Running docker_init.py ==="
python docker_init.py
EXIT_CODE=$?
echo "docker_init.py exited with code: $EXIT_CODE"
echo ""
echo "=== Starting Uvicorn ==="
echo "Command: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
