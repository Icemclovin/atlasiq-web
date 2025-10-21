# 🔐 Test/Developer Account Credentials

## Quick Login Credentials

Use these credentials to quickly test the AtlasIQ Web application:

### Test Account #1

- **Email**: `dev@atlasiq.com`
- **Password**: `developer123`
- **Name**: Developer Account
- **Purpose**: Main developer/testing account

### Test Account #2

- **Email**: `test@atlasiq.com`
- **Password**: `testpass123`
- **Name**: Test User
- **Purpose**: Additional test account

### Test Account #3

- **Email**: `admin@atlasiq.com`
- **Password**: `admin123456`
- **Name**: Admin Account
- **Purpose**: Admin testing

---

## How to Create Account

### Option 1: Via Frontend UI (Recommended)

1. Go to http://localhost:3000/register
2. Fill in the form:
   - Full Name: "Your Name"
   - Email: "your@email.com"
   - Password: "yourpassword" (minimum 8 characters)
   - Confirm Password: "yourpassword"
3. Click "Create Account"
4. You'll be automatically logged in

### Option 2: Via API (For Testing)

```powershell
# Using PowerShell
$body = @{
    email = "newemail@example.com"
    password = "newpassword123"
    full_name = "New User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Option 3: Via Python Script

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/auth/register",
    json={
        "email": "python@example.com",
        "password": "pythonpass123",
        "full_name": "Python User"
    }
)
print(response.json())
```

### Option 4: Via cURL

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "curl@example.com",
    "password": "curlpass123",
    "full_name": "Curl User"
  }'
```

---

## Login Instructions

### Via Frontend

1. Go to http://localhost:3000/login
2. Enter email and password
3. Click "Sign In"

### Via API

```powershell
# PowerShell
$credentials = @{
    email = "dev@atlasiq.com"
    password = "developer123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/login" `
    -Method Post `
    -ContentType "application/json" `
    -Body $credentials

# Access token for API calls
$accessToken = $response.access_token
```

---

## Testing Checklist

### Authentication Flow

- [ ] Register new account
- [ ] Login with credentials
- [ ] Access protected dashboard route
- [ ] Logout successfully
- [ ] Verify redirect to login when logged out

### Dashboard Features

- [ ] View KPI cards
- [ ] See country overview cards
- [ ] Check risk scores (color-coded)
- [ ] View interactive charts
- [ ] Verify responsive design (resize browser)

### API Endpoints

- [ ] POST /api/v1/auth/register - Create account
- [ ] POST /api/v1/auth/login - Get JWT tokens
- [ ] GET /api/v1/auth/me - Get current user
- [ ] GET /api/v1/dashboard/summary - Dashboard data
- [ ] GET /api/v1/countries - List countries
- [ ] GET /api/v1/indicators - List indicators

---

## Important Notes

⚠️ **Database Not Connected**

- User accounts are stored in memory only
- Accounts will be lost when server restarts
- To persist accounts, set up PostgreSQL database

⚠️ **No Real Data Yet**

- Dashboard shows placeholder/demo data
- Real data requires implementing data adapters
- See QUICK_START.md for next steps

✅ **What Works Now**

- Full authentication flow (register, login, logout)
- JWT token management
- Protected routes
- Dashboard UI with charts
- API integration
- Responsive design

---

## Troubleshooting

### "Invalid credentials"

- Check email/password spelling
- Ensure account was created successfully
- Try creating new account

### "Cannot connect to server"

- Verify backend is running on port 8000
- Verify frontend is running on port 3000
- Check browser console for errors

### "Registration failed"

- Check password is 8+ characters
- Ensure passwords match
- Try different email address

---

## Quick Start Commands

### Start Backend

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
npm run dev
```

### Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

**Created**: October 21, 2025  
**For**: AtlasIQ Web Development & Testing  
**Status**: Ready to use ✅
