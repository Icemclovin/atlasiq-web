# 🚀 Quick Commands to Deploy AtlasIQ to GitHub

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `atlasiq-web`
3. Description: `Economic Intelligence Platform for Benelux-DE`
4. **Public** (so others can see it)
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

## Step 2: Push Your Code

Open PowerShell in the project folder and run:

```powershell
# Navigate to project
cd C:\Users\ASUS\Desktop\parfumai\atlasiq-web

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AtlasIQ Web Application"

# Add your GitHub repository
# Replace YOUR-USERNAME with your actual GitHub username!
git remote add origin https://github.com/YOUR-USERNAME/atlasiq-web.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Done! Your code is now on GitHub!** ✅

---

## Step 3: Deploy Backend to Railway

1. Go to https://railway.app/
2. Click "Login" → Sign in with GitHub
3. Click "New Project"
4. Click "Deploy from GitHub repo"
5. Select `atlasiq-web`
6. Click on the service → Settings → Root Directory → `backend`
7. Go to Variables tab, add:
   ```
   DATABASE_URL=sqlite+aiosqlite:///./data/atlasiq.db
   JWT_SECRET_KEY=your-random-secret-32-chars
   JWT_ALGORITHM=HS256
   DEBUG=false
   APP_ENV=production
   ```
8. **Generate JWT secret** (PowerShell):
   ```powershell
   -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
   ```
9. Click "Deploy"
10. Copy your Railway URL: `https://atlasiq-backend-production.up.railway.app`

**Backend is live!** ✅

---

## Step 4: Deploy Frontend to Vercel

1. Go to https://vercel.com/
2. Click "Login" → Sign in with GitHub
3. Click "Add New" → "Project"
4. Import `atlasiq-web` repository
5. Configure:
   - Root Directory: `frontend`
   - Framework Preset: `Vite`
   - Build Command: `npm run build`
   - Output Directory: `dist`
6. Add Environment Variable:
   ```
   Name: VITE_API_BASE_URL
   Value: https://your-railway-url.railway.app
   ```
   (Use your Railway URL from Step 3!)
7. Click "Deploy"
8. Wait ~2 minutes
9. Copy your Vercel URL: `https://atlasiq-username.vercel.app`

**Frontend is live!** ✅

---

## ✅ You're Done!

**Share this URL with anyone:**
```
https://atlasiq-username.vercel.app
```

They can:
- ✅ Access the dashboard
- ✅ Create an account
- ✅ Login and use the app
- ✅ See real data

---

## 🔄 Update Your Deployed App

After making changes:

```powershell
# Commit changes
git add .
git commit -m "Update feature"
git push

# Railway and Vercel automatically redeploy!
```

---

## 🎯 Quick Links After Deployment

- **Your App**: https://atlasiq-username.vercel.app
- **Your API**: https://atlasiq-backend.railway.app
- **API Docs**: https://atlasiq-backend.railway.app/docs
- **GitHub Repo**: https://github.com/YOUR-USERNAME/atlasiq-web

---

## 📱 Share Your App

Send people this message:

```
Check out AtlasIQ - Economic Intelligence Dashboard!
🌐 https://atlasiq-username.vercel.app

Login:
📧 Create your own account or use:
   Email: admin@atlasiq.com
   Password: admin123
```

---

## 💡 Pro Tips

1. **Custom Domain**: Add a custom domain in Vercel settings
2. **Monitoring**: Check Railway logs for backend issues
3. **Analytics**: Add Vercel Analytics in project settings
4. **Auto-deploy**: Every git push auto-updates your site!

---

## 🆘 Troubleshooting

**Frontend can't connect to backend:**
- Check `VITE_API_BASE_URL` in Vercel environment variables
- Make sure you used your Railway URL

**Backend returns 500 error:**
- Check Railway logs
- Verify JWT_SECRET_KEY is set
- Ensure DATABASE_URL is correct

**Need help?**
- See DEPLOYMENT_GUIDE.md
- Check Railway/Vercel dashboard logs
- Open GitHub issue

---

**That's it! Your app is live and shareable!** 🎉
