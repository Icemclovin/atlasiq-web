@echo off
cd /d "%~dp0"
echo Starting AtlasIQ Backend...
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
