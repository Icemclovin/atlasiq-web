# AtlasIQ Docker Management Script
# Convenient commands for managing Docker deployment

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('build', 'start', 'stop', 'restart', 'logs', 'status', 'clean', 'backup', 'test')]
    [string]$Action = 'start'
)

$ComposeFile = "docker-compose.prod.yml"
$ProjectName = "atlasiq-web"

function Write-Header {
    param([string]$Text)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host " $Text" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Test-DockerRunning {
    try {
        docker info | Out-Null
        return $true
    } catch {
        Write-Host "❌ Docker is not running!" -ForegroundColor Red
        Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
        return $false
    }
}

switch ($Action) {
    'build' {
        Write-Header "Building Docker Images"
        docker-compose -f $ComposeFile build
        Write-Host "`n✅ Build complete!" -ForegroundColor Green
    }
    
    'start' {
        Write-Header "Starting AtlasIQ Services"
        
        if (-not (Test-DockerRunning)) { exit 1 }
        
        Write-Host "🔨 Building and starting containers..." -ForegroundColor Yellow
        docker-compose -f $ComposeFile up -d --build
        
        Write-Host "`n⏳ Waiting for services to be healthy..." -ForegroundColor Yellow
        Start-Sleep -Seconds 10
        
        Write-Host "`n📊 Container Status:" -ForegroundColor Cyan
        docker-compose -f $ComposeFile ps
        
        Write-Host "`n✅ AtlasIQ is running!" -ForegroundColor Green
        Write-Host "`n🌐 Access the application:" -ForegroundColor Cyan
        Write-Host "   Frontend: http://localhost" -ForegroundColor White
        Write-Host "   Backend:  http://localhost:8000" -ForegroundColor White
        Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
        Write-Host "`n👤 Default login:" -ForegroundColor Cyan
        Write-Host "   Email:    admin@atlasiq.com" -ForegroundColor White
        Write-Host "   Password: admin123" -ForegroundColor White
        Write-Host "   ⚠️  Please change password after first login!" -ForegroundColor Yellow
    }
    
    'stop' {
        Write-Header "Stopping AtlasIQ Services"
        docker-compose -f $ComposeFile down
        Write-Host "✅ Services stopped!" -ForegroundColor Green
    }
    
    'restart' {
        Write-Header "Restarting AtlasIQ Services"
        docker-compose -f $ComposeFile restart
        Write-Host "✅ Services restarted!" -ForegroundColor Green
    }
    
    'logs' {
        Write-Header "Viewing Logs (Ctrl+C to exit)"
        docker-compose -f $ComposeFile logs -f
    }
    
    'status' {
        Write-Header "Service Status"
        
        Write-Host "📦 Containers:" -ForegroundColor Cyan
        docker-compose -f $ComposeFile ps
        
        Write-Host "`n💾 Volumes:" -ForegroundColor Cyan
        docker volume ls | Select-String "atlasiq"
        
        Write-Host "`n🏥 Health Status:" -ForegroundColor Cyan
        $backendHealth = docker inspect atlasiq-backend --format='{{.State.Health.Status}}' 2>$null
        $frontendHealth = docker inspect atlasiq-frontend --format='{{.State.Health.Status}}' 2>$null
        
        if ($backendHealth) {
            Write-Host "   Backend:  $backendHealth" -ForegroundColor $(if($backendHealth -eq 'healthy'){'Green'}else{'Red'})
        }
        if ($frontendHealth) {
            Write-Host "   Frontend: $frontendHealth" -ForegroundColor $(if($frontendHealth -eq 'healthy'){'Green'}else{'Red'})
        }
        
        Write-Host "`n📊 Resource Usage:" -ForegroundColor Cyan
        docker stats --no-stream atlasiq-backend atlasiq-frontend 2>$null
    }
    
    'clean' {
        Write-Header "Cleaning Up"
        
        $confirm = Read-Host "This will remove all containers, volumes, and images. Are you sure? (yes/no)"
        if ($confirm -eq 'yes') {
            Write-Host "🧹 Removing containers and volumes..." -ForegroundColor Yellow
            docker-compose -f $ComposeFile down -v --rmi all
            Write-Host "✅ Cleanup complete!" -ForegroundColor Green
        } else {
            Write-Host "❌ Cancelled" -ForegroundColor Yellow
        }
    }
    
    'backup' {
        Write-Header "Backing Up Database"
        
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $backupFile = "atlasiq_backup_$timestamp.tar.gz"
        
        Write-Host "💾 Creating backup: $backupFile" -ForegroundColor Yellow
        docker run --rm -v atlasiq-web_backend-data:/data -v ${PWD}:/backup alpine tar czf /backup/$backupFile -C /data .
        
        if (Test-Path $backupFile) {
            Write-Host "✅ Backup created: $backupFile" -ForegroundColor Green
            Write-Host "   Size: $((Get-Item $backupFile).Length / 1KB) KB" -ForegroundColor Cyan
        } else {
            Write-Host "❌ Backup failed!" -ForegroundColor Red
        }
    }
    
    'test' {
        Write-Header "Testing Services"
        
        Write-Host "🔍 Testing backend health..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Backend is healthy" -ForegroundColor Green
            }
        } catch {
            Write-Host "❌ Backend health check failed" -ForegroundColor Red
        }
        
        Write-Host "`n🔍 Testing frontend..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://localhost/" -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ Frontend is accessible" -ForegroundColor Green
            }
        } catch {
            Write-Host "❌ Frontend is not accessible" -ForegroundColor Red
        }
        
        Write-Host "`n🔍 Testing API documentation..." -ForegroundColor Yellow
        try {
            $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-Host "✅ API docs are accessible" -ForegroundColor Green
            }
        } catch {
            Write-Host "❌ API docs are not accessible" -ForegroundColor Red
        }
    }
}

Write-Host ""
