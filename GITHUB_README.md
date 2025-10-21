# 🌍 AtlasIQ Web - GitHub Deployment README

**Complete guide for deploying this repository to GitHub and hosting it online.**

## 🎯 Quick Deploy (3 Commands)

```powershell
# 1. Initialize git and commit
git init
git add .
git commit -m "Initial commit"

# 2. Create repo on GitHub, then push
git remote add origin https://github.com/YOUR-USERNAME/atlasiq-web.git
git branch -M main
git push -u origin main

# 3. Deploy online (see below)
```

## 🚀 Hosting Options (All Free)

### Option 1: Railway + Vercel (⭐ Recommended)

**Backend → Railway** (https://railway.app)
- Free $5/month credit
- Auto-deploys from GitHub
- Get URL like: `https://atlasiq-backend.railway.app`

**Frontend → Vercel** (https://vercel.com)
- Completely free for hobby projects
- Auto-deploys from GitHub
- Get URL like: `https://atlasiq.vercel.app`

### Option 2: Render (All-in-One)

**Both → Render** (https://render.com)
- Free tier for both frontend and backend
- Single platform management
- Get URLs like: `https://atlasiq.onrender.com`

### Option 3: Netlify + Railway

**Frontend → Netlify** (https://netlify.com)
**Backend → Railway** (https://railway.app)

## 📖 Complete Deployment Guide

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for detailed step-by-step instructions.

## 📦 What's Included

✅ **Frontend** - React + TypeScript + Vite  
✅ **Backend** - FastAPI + Python 3.11  
✅ **Database** - SQLite (auto-configured)  
✅ **Docker** - Production-ready containers  
✅ **CI/CD** - GitHub Actions workflows  
✅ **Docs** - Complete deployment guides  

## 🎮 For People Cloning This Repo

### 1. Clone and Setup

```powershell
# Clone the repository
git clone https://github.com/YOUR-USERNAME/atlasiq-web.git
cd atlasiq-web

# Run setup (installs everything)
.\setup.ps1

# Start the application
.\START_ALL.ps1
```

### 2. Access Locally

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 3. Default Login

- Email: `admin@atlasiq.com`
- Password: `admin123`

## 📁 Repository Structure

```
atlasiq-web/
├── backend/              # FastAPI backend
├── frontend/             # React frontend
├── .github/workflows/    # CI/CD automation
├── setup.ps1            # Quick setup script
├── START_ALL.ps1        # Start script
├── DEPLOYMENT_GUIDE.md  # Detailed deployment instructions
├── DOCKER_DEPLOYMENT.md # Docker setup guide
└── README.md            # Project overview
```

## 🔧 Configuration Files

All configuration files are included:

- ✅ `vercel.json` - Vercel deployment
- ✅ `netlify.toml` - Netlify deployment
- ✅ `backend/railway.toml` - Railway deployment
- ✅ `backend/render.yaml` - Render deployment
- ✅ `docker-compose.prod.yml` - Docker production
- ✅ `.github/workflows/` - CI/CD pipelines

## 📊 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React 18, TypeScript, Vite, TailwindCSS |
| Backend | FastAPI, Python 3.11, SQLAlchemy |
| Database | SQLite (development), PostgreSQL (production) |
| Auth | JWT tokens, bcrypt |
| Deployment | Railway, Vercel, Render, Netlify |
| Container | Docker, Docker Compose |

## 🎯 Next Steps

1. **Push to GitHub** (instructions above)
2. **Deploy Backend** → Railway (see DEPLOYMENT_GUIDE.md)
3. **Deploy Frontend** → Vercel (see DEPLOYMENT_GUIDE.md)
4. **Share URL** → Send Vercel link to others!

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Complete deployment instructions
- **[DOCKER_DEPLOYMENT.md](DOCKER_DEPLOYMENT.md)** - Docker setup and usage
- **[DOCKER_SETUP_COMPLETE.md](DOCKER_SETUP_COMPLETE.md)** - Docker quick reference

## 🆘 Need Help?

Check the deployment guide or open an issue!

---

**Ready to deploy? Follow [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)!** 🚀
