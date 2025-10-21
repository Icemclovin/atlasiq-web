# Register test account via API
$body = @{
    email = "dev@atlasiq.com"
    password = "developer123"
    full_name = "Developer Account"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" -Method Post -Body $body -ContentType "application/json"
    Write-Host "SUCCESS! Account created:" -ForegroundColor Green
    Write-Host "  Email: dev@atlasiq.com" -ForegroundColor Cyan
    Write-Host "  Password: developer123" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now login at http://localhost:3000" -ForegroundColor Yellow
} catch {
    $statusCode = $_.Exception.Response.StatusCode.value__
    if ($statusCode -eq 400) {
        Write-Host "Account already exists! You can login with:" -ForegroundColor Yellow
        Write-Host "  Email: dev@atlasiq.com" -ForegroundColor Cyan
        Write-Host "  Password: developer123" -ForegroundColor Cyan
    } else {
        Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}
