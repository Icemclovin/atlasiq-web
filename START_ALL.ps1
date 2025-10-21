# AtlasIQ Web - Start All Services
# This script starts both frontend and backend servers

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AtlasIQ Web - Starting Application" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Kill any existing instances
Write-Host "[0/3] Cleaning up existing processes..." -ForegroundColor Yellow
Stop-Process -Name python,node -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start Backend
Write-Host "[1/3] Starting Backend Server..." -ForegroundColor Yellow
$BackendPath = Join-Path $ScriptDir "backend"
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd /d `"$BackendPath`" && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Wait for backend to initialize
Write-Host "      Waiting for backend..." -ForegroundColor Gray
Start-Sleep -Seconds 6

# Check backend health
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "      Backend: OK ($($health.status))" -ForegroundColor Green
} catch {
    Write-Host "      Backend: Starting (may take a moment)" -ForegroundColor Yellow
}

# Start Frontend
Write-Host "[2/3] Starting Frontend Server..." -ForegroundColor Yellow
$FrontendPath = Join-Path $ScriptDir "frontend"
Start-Process -FilePath "cmd.exe" -ArgumentList "/k", "cd /d `"$FrontendPath`" && npm run dev"

# Wait for frontend to initialize
Write-Host "      Waiting for frontend..." -ForegroundColor Gray
Start-Sleep -Seconds 6

# Check frontend
try {
    $response = Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing -TimeoutSec 5
    Write-Host "      Frontend: OK (HTTP $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "      Frontend: Starting (may take a moment)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Application Ready!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "URLs:" -ForegroundColor Cyan
Write-Host "  Frontend:  http://localhost:3000" -ForegroundColor White
Write-Host "  Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Login Credentials:" -ForegroundColor Cyan
Write-Host "  Email:     dev@atlasiq.com" -ForegroundColor White
Write-Host "  Password:  developer123" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "  1. Go to http://localhost:3000" -ForegroundColor White
Write-Host "  2. Click 'Login'" -ForegroundColor White
Write-Host "  3. Enter the credentials above" -ForegroundColor White
Write-Host "  4. View your dashboard!" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to open in browser..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "[3/3] Opening browser..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "Application is running!" -ForegroundColor Green
Write-Host "To stop: Close the backend and frontend command windows" -ForegroundColor Gray
Write-Host ""
