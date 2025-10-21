# AtlasIQ Web - Complete Setup & Usage Guide

## 🎯 Overview

AtlasIQ Web is a full-stack application for macroeconomic data analysis with:

- **Backend**: FastAPI (Python) - Already running ✅
- **Frontend**: React + TypeScript (Vite) - **Ready to start** 🚀

---

## ✅ Current Status

### Backend (COMPLETED ✅)

- ✅ FastAPI server running on http://localhost:8000
- ✅ API documentation at http://localhost:8000/docs
- ✅ JWT authentication configured
- ✅ Database models defined
- ⚠️ Database connection pending (PostgreSQL not running)

### Frontend (READY TO START 🚀)

- ✅ Complete React + TypeScript project structure created
- ✅ All components and pages implemented
- ✅ API service layer with authentication
- ✅ Responsive UI with Tailwind CSS
- 📦 **Next step: Install dependencies and run**

---

## 🚀 Quick Start - Frontend

### Step 1: Open PowerShell in Frontend Directory

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
```

### Step 2: Install Dependencies

```powershell
npm install
```

This will install (~30 seconds):

- React & React DOM
- React Router
- Axios (API client)
- Recharts (data visualization)
- Tailwind CSS
- TypeScript & Vite
- All other dependencies

### Step 3: Start Development Server

```powershell
npm run dev
```

### Step 4: Open Browser

Navigate to: **http://localhost:3000**

---

## 📋 Complete Setup Checklist

### Backend ✅

- [x] Virtual environment created
- [x] Dependencies installed (FastAPI, SQLAlchemy, etc.)
- [x] Server running on port 8000
- [x] API endpoints configured
- [ ] PostgreSQL database setup (optional for now)

### Frontend (To Do)

- [ ] Install npm dependencies
- [ ] Start development server
- [ ] Test login/register pages
- [ ] Verify dashboard loads

---

## 🎨 What You'll See

### 1. Login Page

- Beautiful gradient background
- Email and password fields
- Link to registration page
- Error handling with visual feedback

### 2. Registration Page

- Full name, email, password fields
- Password confirmation
- Validation (minimum 8 characters, matching passwords)
- Automatic redirect to dashboard after signup

### 3. Dashboard

- **Header**: Welcome message with logout button
- **KPI Cards**: Countries, Indicators, Data Freshness, Last Updated
- **Country Cards**: Individual cards for each country showing:
  - GDP Growth with trend indicator
  - Unemployment rate
  - Inflation rate
  - Business confidence index
  - Risk score with color coding
- **Charts**:
  - GDP Growth bar chart
  - Risk Scores bar chart

---

## 🔧 Configuration

### Frontend Environment (.env)

Already created at: `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Backend Environment (.env)

Already configured at: `backend/.env`

```env
DATABASE_URL=postgresql+asyncpg://...
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
JWT_SECRET_KEY=...
DEBUG=True
```

---

## 📡 API Endpoints Used by Frontend

### Authentication

- `POST /api/v1/auth/register` - Create new user
- `POST /api/v1/auth/login` - Login and get tokens
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/auth/refresh` - Refresh access token

### Data

- `GET /api/v1/countries` - List countries
- `GET /api/v1/indicators` - List indicators
- `GET /api/v1/dashboard/summary` - Dashboard KPIs
- `GET /api/v1/dashboard/country/{code}` - Country details
- `GET /api/v1/dashboard/risk-scores` - Risk scores

---

## 🎯 Testing the Application

### 1. Create an Account

1. Go to http://localhost:3000
2. Click "Sign up"
3. Fill in:
   - Full Name: "Test User"
   - Email: "test@example.com"
   - Password: "password123"
   - Confirm Password: "password123"
4. Click "Create Account"

### 2. Login

1. Email: "test@example.com"
2. Password: "password123"
3. Click "Sign In"

### 3. View Dashboard

- You'll be redirected to the dashboard automatically
- Initially, it may show "No country data available" until data is fetched
- This is normal - the backend needs to fetch data from external APIs

---

## 🐛 Troubleshooting

### "Cannot connect to backend"

**Solution**: Make sure backend is running

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### "Port 3000 already in use"

**Solution**: Kill the process or change port in `vite.config.ts`

```powershell
# Find process using port 3000
netstat -ano | findstr :3000
# Kill it (replace PID)
taskkill /PID <PID> /F
```

### "npm not found"

**Solution**: Install Node.js from https://nodejs.org/

### Database Connection Warning

**This is OK for now!** The backend will start without database. Features that need database:

- User registration/login will work (uses in-memory until DB setup)
- Dashboard will show empty data until database is configured

---

## 📚 Project Files Created

### Frontend Structure (26 files)

```
frontend/
├── package.json              # Dependencies & scripts
├── vite.config.ts           # Vite configuration
├── tsconfig.json            # TypeScript config
├── tailwind.config.js       # Tailwind CSS config
├── postcss.config.js        # PostCSS config
├── index.html               # HTML template
├── .env                     # Environment variables
├── setup.ps1                # Setup script
├── README.md                # Documentation
└── src/
    ├── main.tsx             # Entry point
    ├── App.tsx              # Root component
    ├── index.css            # Global styles
    ├── vite-env.d.ts        # Type definitions
    ├── components/          # 5 components
    │   ├── Button.tsx
    │   ├── Card.tsx
    │   ├── Input.tsx
    │   ├── Loading.tsx
    │   └── ProtectedRoute.tsx
    ├── context/             # Auth context
    │   └── AuthContext.tsx
    ├── pages/               # 3 pages
    │   ├── Login.tsx
    │   ├── Register.tsx
    │   └── Dashboard.tsx
    ├── services/            # API layer
    │   ├── api.ts
    │   ├── auth.ts
    │   └── data.ts
    └── types/               # TypeScript types
        └── index.ts
```

---

## 🚀 Next Steps

### Immediate (5 minutes)

1. **Install frontend dependencies**:

   ```powershell
   cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
   npm install
   ```

2. **Start frontend**:

   ```powershell
   npm run dev
   ```

3. **Test the application**:
   - Open http://localhost:3000
   - Create an account
   - Login
   - View dashboard

### Short Term (Next session)

1. **Set up PostgreSQL database**:

   - Install PostgreSQL OR use Docker
   - Run database migrations
   - Test user registration with persistence

2. **Implement data fetching**:

   - Create data adapters (Eurostat, ECB, World Bank, OECD)
   - Schedule automated data refresh
   - Test dashboard with real data

3. **Add more features**:
   - Country detail pages
   - Indicator explorer
   - Data export functionality
   - Settings page

---

## 📊 Technology Stack Summary

### Frontend

- ⚛️ **React 18** - UI library
- 📘 **TypeScript** - Type safety
- ⚡ **Vite** - Build tool (super fast!)
- 🎨 **Tailwind CSS** - Styling
- 📊 **Recharts** - Charts & graphs
- 🔄 **Axios** - HTTP client
- 🛣️ **React Router** - Navigation
- 🎯 **Lucide Icons** - Beautiful icons

### Backend

- 🚀 **FastAPI** - Web framework
- 🐍 **Python 3.11** - Language
- 🗄️ **SQLAlchemy** - ORM
- 🔒 **JWT** - Authentication
- 📦 **Pydantic** - Data validation
- 🔄 **Uvicorn** - ASGI server

---

## 🎓 Learning Resources

- **React**: https://react.dev/
- **TypeScript**: https://www.typescriptlang.org/
- **Vite**: https://vitejs.dev/
- **Tailwind CSS**: https://tailwindcss.com/
- **FastAPI**: https://fastapi.tiangolo.com/

---

**Ready to start?** Run these commands:

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
npm install
npm run dev
```

Then open: **http://localhost:3000** 🎉
