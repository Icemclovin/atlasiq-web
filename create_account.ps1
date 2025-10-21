# AtlasIQ Web - Create Test Account Script
# Quick script to create test/developer accounts

param(
    [string]$Email = "dev@atlasiq.com",
    [string]$Password = "developer123",
    [string]$FullName = "Developer Account"
)

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  AtlasIQ Web - Create Test Account" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Creating account with:" -ForegroundColor Yellow
Write-Host "  Email: $Email" -ForegroundColor White
Write-Host "  Password: $Password" -ForegroundColor White
Write-Host "  Name: $FullName" -ForegroundColor White
Write-Host ""

$body = @{
    email = $Email
    password = $Password
    full_name = $FullName
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" `
        -Method Post `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "✅ SUCCESS! Account created" -ForegroundColor Green
    Write-Host ""
    Write-Host "Login credentials:" -ForegroundColor Cyan
    Write-Host "  Email: $Email" -ForegroundColor White
    Write-Host "  Password: $Password" -ForegroundColor White
    Write-Host ""
    Write-Host "Login at: http://localhost:3000/login" -ForegroundColor Yellow
    Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "Response:" -ForegroundColor Gray
    Write-Host ($response | ConvertTo-Json -Depth 3) -ForegroundColor DarkGray
    
} catch {
    Write-Host "❌ ERROR: Could not create account" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "  - Backend server not running (start with: npm run dev:backend)" -ForegroundColor White
    Write-Host "  - Account already exists (try different email)" -ForegroundColor White
    Write-Host "  - Invalid email/password format" -ForegroundColor White
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Gray
    Write-Host $_.Exception.Message -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Examples of usage:
Write-Host "Usage examples:" -ForegroundColor Yellow
Write-Host "  .\create_account.ps1" -ForegroundColor Gray
Write-Host "  .\create_account.ps1 -Email 'test@example.com' -Password 'testpass123' -FullName 'Test User'" -ForegroundColor Gray
Write-Host ""
