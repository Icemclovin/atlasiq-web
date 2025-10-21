# AtlasIQ Backend Startup Script
# This script starts the FastAPI backend server

Write-Host "Starting AtlasIQ Backend..." -ForegroundColor Cyan

# Get the script's directory
$BackendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $BackendDir

Write-Host "Working Directory: $BackendDir" -ForegroundColor Green

# Check if app directory exists
if (Test-Path ".\app\main.py") {
    Write-Host "Found app/main.py" -ForegroundColor Green
} else {
    Write-Host "Error: app/main.py not found!" -ForegroundColor Red
    Write-Host "Current directory: $(Get-Location)" -ForegroundColor Yellow
    exit 1
}

# Start uvicorn
Write-Host "Starting Uvicorn server on http://0.0.0.0:8000..." -ForegroundColor Cyan
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
