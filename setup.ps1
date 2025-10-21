# Quick Setup Script for AtlasIQ Web
# Run this after cloning the repository

Write-Host @"
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║          AtlasIQ Web - Quick Setup Script                ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"@ -ForegroundColor Cyan

Write-Host "`n🚀 Setting up AtlasIQ Web Application...`n" -ForegroundColor Green

# Check Python
Write-Host "📦 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.11+" -ForegroundColor Red
    exit 1
}

# Check Node.js
Write-Host "`n📦 Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✅ Node.js $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js not found! Please install Node.js 18+" -ForegroundColor Red
    exit 1
}

# Setup Backend
Write-Host "`n🔧 Setting up Backend..." -ForegroundColor Yellow
Write-Host "   Installing Python dependencies..." -ForegroundColor Gray
cd backend
pip install -r requirements.txt --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install backend dependencies" -ForegroundColor Red
    exit 1
}

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "   Creating .env file..." -ForegroundColor Gray
    $jwtSecret = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
    @"
DATABASE_URL=sqlite+aiosqlite:///./atlasiq.db
JWT_SECRET_KEY=$jwtSecret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=true
APP_ENV=development
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file" -ForegroundColor Green
}

# Initialize database and create admin account
Write-Host "   Initializing database..." -ForegroundColor Gray
python docker_init.py
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database initialized" -ForegroundColor Green
} else {
    Write-Host "⚠️  Database initialization had issues (may be normal if already exists)" -ForegroundColor Yellow
}

cd ..

# Setup Frontend
Write-Host "`n🎨 Setting up Frontend..." -ForegroundColor Yellow
Write-Host "   Installing Node.js dependencies (this may take a few minutes)..." -ForegroundColor Gray
cd frontend
npm install --silent
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install frontend dependencies" -ForegroundColor Red
    exit 1
}

# Create .env if not exists
if (-not (Test-Path ".env")) {
    Write-Host "   Creating .env file..." -ForegroundColor Gray
    @"
VITE_API_BASE_URL=http://localhost:8000
"@ | Out-File -FilePath ".env" -Encoding UTF8
    Write-Host "✅ Created .env file" -ForegroundColor Green
}

cd ..

# Success message
Write-Host @"

╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                  ✅ Setup Complete!                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🚀 To start the application:

   Option 1: Use the start script (recommended)
   .\START_ALL.ps1

   Option 2: Start manually in two terminals

   Terminal 1 (Backend):
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   Terminal 2 (Frontend):
   cd frontend
   npm run dev

📱 Access the application:
   Frontend: http://localhost:3000
   Backend:  http://localhost:8000
   API Docs: http://localhost:8000/docs

👤 Default login:
   Email:    admin@atlasiq.com
   Password: admin123
   ⚠️  Change password after first login!

📖 For more information:
   - README.md           - Project overview
   - DEPLOYMENT_GUIDE.md - Deploy online
   - DOCKER_DEPLOYMENT.md - Docker setup

"@ -ForegroundColor Cyan

Write-Host "Happy coding! 🎉`n" -ForegroundColor Green
