# 🚀 Deploy AtlasIQ to GitHub and Host Online

Complete guide to deploy your AtlasIQ system so others can access it via a live URL.

## 📋 Overview

We'll deploy:
- **Frontend** → Vercel or Netlify (Free, automatic HTTPS)
- **Backend** → Railway or Render (Free tier available)
- **Code** → GitHub (Free, version control)

## 🎯 Quick Start (3 Steps)

### Step 1: Push to GitHub
```powershell
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AtlasIQ Web Application"

# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR-USERNAME/atlasiq-web.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy Backend (Railway - Easiest)
1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `atlasiq-web` repository
5. Railway auto-detects the backend
6. Add environment variables:
   - `DATABASE_URL`: `sqlite+aiosqlite:///./data/atlasiq.db`
   - `JWT_SECRET_KEY`: Generate random string
7. Deploy! Get URL like: `https://atlasiq-backend.railway.app`

### Step 3: Deploy Frontend (Vercel - Easiest)
1. Go to https://vercel.com/
2. Sign in with GitHub
3. Click "New Project" → Import your repository
4. Configure:
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add environment variable:
   - `VITE_API_BASE_URL`: Your Railway backend URL
6. Deploy! Get URL like: `https://atlasiq.vercel.app`

**Done! Share your Vercel URL with anyone!** 🎉

---

## 📝 Detailed Instructions

### Option A: Railway (Backend) + Vercel (Frontend) ⭐ RECOMMENDED

#### 1. Create GitHub Repository

```powershell
# Navigate to project
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AtlasIQ Web Application"
```

Go to https://github.com/new and create a repository named `atlasiq-web`

```powershell
# Link to GitHub
git remote add origin https://github.com/YOUR-USERNAME/atlasiq-web.git
git branch -M main
git push -u origin main
```

#### 2. Deploy Backend to Railway

**Why Railway?**
- ✅ Free $5/month credit
- ✅ Auto-detects Python
- ✅ Easy environment variables
- ✅ Automatic HTTPS
- ✅ Good free tier

**Steps:**

1. **Sign up**: Go to https://railway.app/ and sign in with GitHub

2. **Create Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `atlasiq-web`
   - Railway will detect the backend automatically

3. **Configure Service**:
   - Click on the backend service
   - Go to "Settings" → "Root Directory" → Set to `backend`

4. **Environment Variables** (Settings → Variables):
   ```
   DATABASE_URL=sqlite+aiosqlite:///./data/atlasiq.db
   JWT_SECRET_KEY=your-secret-key-generate-this
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=false
   APP_ENV=production
   PORT=8000
   ```

5. **Generate JWT Secret** (PowerShell):
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
   ```

6. **Deploy**:
   - Click "Deploy"
   - Wait ~2 minutes
   - Get your URL: `https://atlasiq-backend-production.up.railway.app`

7. **Test**:
   ```powershell
   curl https://your-backend-url.railway.app/health
   ```

#### 3. Deploy Frontend to Vercel

**Why Vercel?**
- ✅ Completely free for hobby projects
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-deploys on git push
- ✅ Zero configuration

**Steps:**

1. **Sign up**: Go to https://vercel.com/ and sign in with GitHub

2. **Import Project**:
   - Click "Add New" → "Project"
   - Import `atlasiq-web` repository
   - Click "Import"

3. **Configure Build**:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`

4. **Environment Variables**:
   ```
   VITE_API_BASE_URL=https://your-railway-backend-url.railway.app
   ```

5. **Deploy**:
   - Click "Deploy"
   - Wait ~1 minute
   - Get your URL: `https://atlasiq.vercel.app`

6. **Test**:
   - Open the Vercel URL
   - Login with: `admin@atlasiq.com` / `admin123`

**✅ Your app is now live! Share the Vercel URL!**

---

### Option B: Render (All-in-One)

Render can host both frontend and backend on free tier.

#### 1. Deploy to Render

1. **Sign up**: https://render.com/ with GitHub

2. **Create Web Service** (Backend):
   - Click "New" → "Web Service"
   - Connect GitHub repository
   - Name: `atlasiq-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python docker_init.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Plan: `Free`

3. **Environment Variables**:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./data/atlasiq.db
   JWT_SECRET_KEY=(generate random string)
   JWT_ALGORITHM=HS256
   DEBUG=false
   ```

4. **Create Static Site** (Frontend):
   - Click "New" → "Static Site"
   - Connect same repository
   - Name: `atlasiq-frontend`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`

5. **Environment Variable**:
   ```
   VITE_API_BASE_URL=https://atlasiq-backend.onrender.com
   ```

**Done! Get URLs:**
- Backend: `https://atlasiq-backend.onrender.com`
- Frontend: `https://atlasiq-frontend.onrender.com`

---

### Option C: Netlify (Frontend) + Railway (Backend)

Similar to Vercel + Railway, but using Netlify for frontend.

1. **Backend**: Follow Railway steps above

2. **Frontend on Netlify**:
   - Go to https://www.netlify.com/
   - Sign in with GitHub
   - "Add new site" → "Import from Git"
   - Select repository
   - Base directory: `frontend`
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Environment variable: `VITE_API_BASE_URL=your-railway-url`

---

## 🔧 Configuration Files Reference

### Backend Environment Variables

Required for any hosting platform:

```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///./data/atlasiq.db

# JWT (CHANGE THESE!)
JWT_SECRET_KEY=your-super-secret-random-key-minimum-32-characters
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Application
APP_ENV=production
DEBUG=false

# Optional: Admin account (created on first run)
ADMIN_EMAIL=admin@atlasiq.com
ADMIN_PASSWORD=admin123
ADMIN_NAME=Administrator
```

### Frontend Environment Variables

```bash
# Backend URL (set to your deployed backend)
VITE_API_BASE_URL=https://your-backend-url.railway.app
```

---

## 📊 Free Tier Limits

| Platform | Frontend | Backend | Database | Bandwidth |
|----------|----------|---------|----------|-----------|
| **Vercel** | ✅ Unlimited | - | - | 100GB/month |
| **Netlify** | ✅ Unlimited | - | - | 100GB/month |
| **Railway** | - | ✅ $5/month credit | ✅ Included | ✅ Included |
| **Render** | ✅ 100GB | ✅ 750hrs/month | ✅ Included | ✅ Included |

**Recommended Combination:**
- Frontend: Vercel (fastest, best DX)
- Backend: Railway (easiest setup, good free tier)

---

## 🔒 Security Checklist

Before deploying:

- [ ] Change default admin password after first login
- [ ] Generate strong JWT secret (32+ characters)
- [ ] Set `DEBUG=false` in production
- [ ] Review CORS settings in backend
- [ ] Don't commit `.env` files (already in .gitignore)
- [ ] Use HTTPS URLs (automatic with these platforms)

---

## 🚀 Automated Deployment

Once set up, every `git push` auto-deploys:

```powershell
# Make changes
# ...

# Commit and push
git add .
git commit -m "Update feature"
git push

# Vercel/Netlify/Railway automatically redeploy!
```

---

## 📱 Custom Domain (Optional)

### Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Railway
1. Go to Settings → Domains
2. Add custom domain
3. Update DNS records

---

## 🐛 Troubleshooting

### Backend won't start
```powershell
# Check logs on Railway
# Common issues:
- DATABASE_URL not set
- JWT_SECRET_KEY missing
- Port not set (Railway sets $PORT automatically)
```

### Frontend can't connect to backend
```powershell
# Check environment variable
VITE_API_BASE_URL=https://your-backend.railway.app

# Check CORS in backend
# Ensure backend allows frontend origin
```

### Database errors
```powershell
# For SQLite on free hosting, data persists in volumes
# But free tiers might reset
# Consider upgrading or using PostgreSQL
```

---

## 💡 Pro Tips

1. **Use Railway for backend**: Best free tier for Python apps
2. **Use Vercel for frontend**: Fastest deploys, best DX
3. **Custom domain**: Makes it look professional
4. **Monitoring**: Use Railway logs to track issues
5. **Auto-deploy**: Connect GitHub for automatic updates

---

## 📖 Quick Reference

### Deploy Commands
```powershell
# Push to GitHub
git add .
git commit -m "message"
git push

# Check deployment status
# Railway: https://railway.app/dashboard
# Vercel: https://vercel.com/dashboard
```

### Test Deployed App
```powershell
# Backend health
curl https://your-backend.railway.app/health

# Frontend
curl https://your-app.vercel.app/

# API docs
# Open: https://your-backend.railway.app/docs
```

---

## ✅ Success Checklist

- [ ] Code pushed to GitHub
- [ ] Backend deployed and health check passes
- [ ] Frontend deployed and loads
- [ ] Login works with admin account
- [ ] Dashboard displays data
- [ ] Share URL with others!

---

## 🆘 Need Help?

1. **Railway Issues**: Check https://railway.app/legal/fair-use
2. **Vercel Issues**: Check https://vercel.com/docs
3. **GitHub Issues**: Check repository Issues tab

---

**Your app will be live at:**
- Frontend: `https://your-app.vercel.app`
- Backend: `https://your-backend.railway.app`

**Share the frontend URL with anyone!** 🎉
