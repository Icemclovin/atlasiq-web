# AtlasIQ Web Backend - Quick Setup Script
# Run this script to set up the backend environment

Write-Host "🚀 AtlasIQ Web Backend - Setup Script" -ForegroundColor Cyan
Write-Host "======================================`n" -ForegroundColor Cyan

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green

# Navigate to backend directory
$backendDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $backendDir
Write-Host "✓ Working directory: $backendDir`n" -ForegroundColor Green

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️  Virtual environment already exists" -ForegroundColor Yellow
    $response = Read-Host "Delete and recreate? (y/n)"
    if ($response -eq 'y') {
        Remove-Item -Recurse -Force venv
        python -m venv venv
        Write-Host "✓ Virtual environment recreated" -ForegroundColor Green
    }
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`nActivating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host "`nUpgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Copy environment file
Write-Host "`nSetting up environment..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
} else {
    Copy-Item ".env.development" ".env"
    Write-Host "✓ Environment file created (.env)" -ForegroundColor Green
    Write-Host "  Edit .env to configure database connection" -ForegroundColor Gray
}

# Check if PostgreSQL is available
Write-Host "`nChecking database..." -ForegroundColor Yellow
$dockerRunning = docker ps 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Docker is running" -ForegroundColor Green
    
    # Check if postgres container exists
    $postgresContainer = docker ps --filter "name=postgres" --format "{{.Names}}" 2>$null
    if ($postgresContainer) {
        Write-Host "✓ PostgreSQL container is running" -ForegroundColor Green
    } else {
        Write-Host "⚠️  PostgreSQL container not found" -ForegroundColor Yellow
        Write-Host "  Run: docker-compose up -d postgres" -ForegroundColor Gray
    }
} else {
    Write-Host "⚠️  Docker is not running" -ForegroundColor Yellow
    Write-Host "  Start Docker Desktop or install PostgreSQL manually" -ForegroundColor Gray
}

# Display next steps
Write-Host "`n======================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host "======================================`n" -ForegroundColor Cyan

Write-Host "📝 Next Steps:`n" -ForegroundColor Yellow

Write-Host "1. Configure environment (if needed):" -ForegroundColor White
Write-Host "   notepad .env`n" -ForegroundColor Gray

Write-Host "2. Start PostgreSQL (if using Docker):" -ForegroundColor White
Write-Host "   cd .." -ForegroundColor Gray
Write-Host "   docker-compose up -d postgres`n" -ForegroundColor Gray

Write-Host "3. Test the backend:" -ForegroundColor White
Write-Host "   python test_backend_core.py`n" -ForegroundColor Gray

Write-Host "4. Start the server:" -ForegroundColor White
Write-Host "   python -m app.main`n" -ForegroundColor Gray

Write-Host "5. Access API docs:" -ForegroundColor White
Write-Host "   http://localhost:8000/docs`n" -ForegroundColor Gray

Write-Host "======================================`n" -ForegroundColor Cyan
Write-Host "Happy coding! 🎉" -ForegroundColor Cyan
