#!/bin/sh
# Startup script for Railway deployment

echo "🚀 Starting AtlasIQ Backend..."
echo "Running database initialization..."

# Run database initialization
# Note: docker_init.py calls sys.exit() so we need to handle that
if python docker_init.py; then
    echo "✅ Database initialization succeeded"
else
    echo "⚠️  Database initialization exited with code $?, continuing anyway..."
fi

# Start uvicorn with Railway's PORT or default to 8000
PORT=${PORT:-8000}
echo ""
echo "🌐 Starting Uvicorn server on port $PORT"
echo "=" * 50
exec uvicorn app.main:app --host 0.0.0.0 --port $PORT
