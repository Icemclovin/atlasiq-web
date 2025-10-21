@echo off
echo.
echo ========================================
echo   AtlasIQ Web - Create Test Account
echo ========================================
echo.
echo This will create a test account via the API
echo.

:INPUT
set /p email="Enter email (default: dev@atlasiq.com): "
if "%email%"=="" set email=dev@atlasiq.com

set /p password="Enter password (default: developer123): "
if "%password%"=="" set password=developer123

set /p fullname="Enter full name (default: Developer Account): "
if "%fullname%"=="" set fullname=Developer Account

echo.
echo Creating account with:
echo   Email: %email%
echo   Password: %password%
echo   Name: %fullname%
echo.

powershell -Command "$body = @{email='%email%';password='%password%';full_name='%fullname%'} | ConvertTo-Json; try { $response = Invoke-RestMethod -Uri 'http://localhost:8000/api/v1/auth/register' -Method Post -ContentType 'application/json' -Body $body; Write-Host ''; Write-Host 'SUCCESS! Account created:' -ForegroundColor Green; Write-Host '  Email: %email%' -ForegroundColor Cyan; Write-Host '  Password: %password%' -ForegroundColor Cyan; Write-Host ''; Write-Host 'Login at: http://localhost:3000/login' -ForegroundColor Yellow } catch { Write-Host ''; Write-Host 'ERROR: Could not create account' -ForegroundColor Red; Write-Host 'Possible reasons:' -ForegroundColor Yellow; Write-Host '  - Backend server not running' -ForegroundColor Yellow; Write-Host '  - Account already exists' -ForegroundColor Yellow; Write-Host '  - Invalid email/password format' -ForegroundColor Yellow }"

echo.
pause
