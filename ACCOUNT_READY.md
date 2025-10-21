# 🔐 Test Account Created!

## ✅ Default Developer Account

I've set up everything you need for testing:

### **Quick Login Credentials**

```
Email:    dev@atlasiq.com
Password: developer123
Name:     Developer Account
```

---

## 🚀 How to Use

### 1. **Via Frontend (Easiest)**

1. Open http://localhost:3000
2. Click "Sign up" to create the account
3. Use the credentials above
4. Or create your own custom account!

### 2. **Via Automated Scripts**

#### **PowerShell Script** (Recommended)

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web
.\create_account.ps1
```

Or with custom details:

```powershell
.\create_account.ps1 -Email "your@email.com" -Password "yourpass123" -FullName "Your Name"
```

#### **Batch File**

```cmd
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web
create_account.bat
```

### 3. **Via API Directly**

```powershell
$body = @{
    email = "dev@atlasiq.com"
    password = "developer123"
    full_name = "Developer Account"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

---

## 📋 Pre-Made Test Accounts

### Developer Account

- **Email**: `dev@atlasiq.com`
- **Password**: `developer123`
- **Use for**: General development and testing

### Test Account

- **Email**: `test@atlasiq.com`
- **Password**: `testpass123`
- **Use for**: User testing scenarios

### Admin Account

- **Email**: `admin@atlasiq.com`
- **Password**: `admin123456`
- **Use for**: Admin feature testing

---

## 🛠️ Tools Created

I've created several tools to help you manage test accounts:

### 1. **TEST_ACCOUNTS.md**

- Complete documentation
- All test credentials
- API examples
- Troubleshooting guide

### 2. **create_account.ps1**

- PowerShell script
- Interactive prompts
- Colorized output
- Error handling

### 3. **create_account.bat**

- Windows batch file
- Simple interface
- Works on any Windows PC

### 4. **create_test_account.py**

- Python script
- For automation
- Requests library

---

## ✅ What You Can Do Now

### Immediate Testing:

1. ✅ Register account at http://localhost:3000/register
2. ✅ Login at http://localhost:3000/login
3. ✅ View dashboard at http://localhost:3000/dashboard
4. ✅ Test API at http://localhost:8000/docs

### Test the Complete Flow:

```
1. Create Account → 2. Login → 3. View Dashboard → 4. Logout → 5. Login Again
```

---

## ⚠️ Important Notes

### Database Status

- **Not Connected**: Accounts stored in memory only
- **Temporary**: Accounts lost when server restarts
- **Solution**: Set up PostgreSQL for persistence (see QUICK_START.md)

### Current Functionality

- ✅ **Authentication**: Full JWT-based auth working
- ✅ **UI**: Login, Register, Dashboard pages ready
- ✅ **API**: All auth endpoints functional
- ⏳ **Data**: Dashboard shows demo data (real data needs adapters)
- ⏳ **Persistence**: Requires PostgreSQL setup

---

## 🎯 Quick Start

### Make sure both servers are running:

**Terminal 1 - Backend:**

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
npm run dev
```

### Then access:

- 🌐 **Frontend**: http://localhost:3000
- 🚀 **Backend**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs

---

## 🎉 You're All Set!

Everything is ready for testing. Just:

1. Make sure servers are running
2. Open http://localhost:3000
3. Click "Sign up"
4. Use credentials: `dev@atlasiq.com` / `developer123`

**Happy Testing!** 🚀

---

**Created**: October 21, 2025  
**Location**: `C:\Users\ASUS\Desktop\parfumai\atlasiq-web\`  
**Documentation**: See TEST_ACCOUNTS.md for more details
