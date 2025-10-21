# 🚀 AtlasIQ Web - Quick Start Card

## ⚡ Start Everything (Copy & Paste)

### Backend (Already Running ✅)

```powershell
# If you need to restart it:
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\backend
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (Start Now 🚀)

```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web\frontend
npm install
npm run dev
```

## 🌐 URLs

| Service             | URL                          |
| ------------------- | ---------------------------- |
| 🎨 **Frontend**     | http://localhost:3000        |
| 🚀 **Backend API**  | http://localhost:8000        |
| 📚 **API Docs**     | http://localhost:8000/docs   |
| ❤️ **Health Check** | http://localhost:8000/health |

## 📝 Test Account

Create a test account at http://localhost:3000/register:

- **Name**: Test User
- **Email**: test@example.com
- **Password**: password123

## 📊 What You Built

### Frontend (26 files)

- ✅ Login & Register pages
- ✅ Dashboard with charts
- ✅ JWT authentication
- ✅ Responsive design
- ✅ TypeScript + React 18

### Backend (19 files)

- ✅ FastAPI REST API
- ✅ JWT authentication
- ✅ SQLAlchemy models
- ✅ CORS configured
- ✅ API documentation

## 🎯 Features

### Authentication

- User registration
- Login with JWT tokens
- Auto token refresh
- Protected routes
- Persistent sessions

### Dashboard

- KPI cards (Countries, Indicators, etc.)
- Country overview cards
- Risk scores (color-coded)
- Interactive bar charts
- Responsive grid layout

### API Integration

- Axios HTTP client
- Request interceptors
- Automatic retries
- Error handling
- Type-safe responses

## 🛠️ Common Commands

### Frontend

```powershell
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run build  # includes type checking
```

### Backend

```powershell
# Start server
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload

# Install package
.\venv\Scripts\pip.exe install package-name

# Check server status
curl http://localhost:8000/health
```

## 🔧 Troubleshooting

### Frontend won't start

```powershell
# Delete node_modules and reinstall
rm -r node_modules
npm install
```

### Backend connection error

1. Check backend is running on port 8000
2. Check CORS settings in backend `.env`
3. Check browser console for errors

### Port already in use

```powershell
# Find and kill process on port 3000
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

## 📁 Key Files

### Frontend

- `src/App.tsx` - Main app with routing
- `src/pages/Login.tsx` - Login page
- `src/pages/Dashboard.tsx` - Dashboard
- `src/services/api.ts` - API client
- `src/context/AuthContext.tsx` - Auth state

### Backend

- `app/main.py` - FastAPI app
- `app/api/v1/auth.py` - Auth endpoints
- `app/models/` - Database models
- `app/services/` - Business logic
- `.env` - Configuration

## 📚 Documentation

1. **FRONTEND_COMPLETE.md** - Full implementation details
2. **FRONTEND_SETUP.md** - Complete setup guide
3. **frontend/README.md** - Developer docs
4. **Backend API Docs** - http://localhost:8000/docs

## ⚠️ Current Status

### Working ✅

- Frontend fully functional
- Backend API running
- Authentication flow
- Dashboard UI
- Charts and visualization

### Pending ⏳

- PostgreSQL database setup
- Real data from APIs
- Data fetching automation
- Background jobs

## 🎯 Next Session Tasks

1. **Set up PostgreSQL**

   - Install PostgreSQL or use Docker
   - Update DATABASE_URL
   - Run migrations
   - Test with real data

2. **Implement Data Adapters**

   - Eurostat adapter
   - ECB adapter
   - World Bank adapter
   - OECD adapter

3. **Schedule Data Fetching**
   - APScheduler setup
   - Automated refresh
   - Error handling

## 💡 Tips

- **Hot Reload**: Both servers auto-reload on changes
- **TypeScript**: Frontend is fully typed - use IDE autocomplete
- **API Docs**: Interactive docs at /docs endpoint
- **Tokens**: Stored in localStorage, cleared on logout
- **CORS**: Already configured for localhost:3000

## 🎉 Success Criteria

You'll know it's working when:

- ✅ Frontend loads at localhost:3000
- ✅ Can create an account
- ✅ Can login successfully
- ✅ Dashboard displays (even if empty)
- ✅ Charts render correctly
- ✅ Logout works

## 🚀 Deploy (Future)

### Frontend

- Vercel, Netlify, GitHub Pages
- Just run `npm run build`
- Upload `dist/` folder

### Backend

- Docker container
- Cloud services (AWS, GCP, Azure)
- VPS with systemd

---

**Created**: October 21, 2025  
**Stack**: React + TypeScript + FastAPI + Python  
**Status**: ✅ READY TO RUN

**Start now**: `cd frontend && npm install && npm run dev` 🚀
