# Vercel Frontend Deployment Guide

## 🎯 Your Backend is Ready!
- **Backend URL**: https://atlasiq-web-production.up.railway.app
- **API Docs**: https://atlasiq-web-production.up.railway.app/docs
- **Health**: https://atlasiq-web-production.up.railway.app/health
- **Login**: admin@atlasiq.com / admin123

---

## 🚀 Deploy Frontend to Vercel

### Option 1: Update Existing Vercel Project (Recommended)

Since you already have a Vercel project named "atlasiq-web":

1. **Go to Vercel**: https://vercel.com/dashboard
2. **Find your project**: Click on "atlasiq-web"
3. **Go to Settings** → **Environment Variables**
4. **Add/Update this variable**:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://atlasiq-web-production.up.railway.app`
   - **Environment**: Production, Preview, Development (select all)
5. **Click Save**
6. **Go to Deployments tab**
7. **Click on the latest deployment** → **3 dots menu** → **Redeploy**

### Option 2: Create New Vercel Project with Different Name

1. **Go to Vercel**: https://vercel.com/
2. **Sign in with GitHub**
3. **Click "Add New Project"**
4. **Import** `Icemclovin/atlasiq-web` repository
5. **Change project name** to something like:
   - `atlasiq-web-app`
   - `atlasiq-dashboard`
   - `atlasiq-prod`
6. **Configure Project**:
   - **Root Directory**: Leave empty (Vercel will auto-detect)
   - **Framework Preset**: Vite
   - **Build Command**: `cd frontend && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`

7. **Environment Variables**:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://atlasiq-web-production.up.railway.app`

8. **Click "Deploy"**

---

## ⚙️ Vercel Configuration Settings

If Vercel doesn't auto-detect correctly, use these manual settings:

### Build & Development Settings
```
Build Command: cd frontend && npm run build
Output Directory: frontend/dist
Install Command: cd frontend && npm install
Development Command: cd frontend && npm run dev
```

### Root Directory
Leave as: `.` (root of repository)

### Framework Preset
Select: **Vite**

---

## 🔧 Environment Variables

Add this in Vercel Settings → Environment Variables:

| Name | Value |
|------|-------|
| VITE_API_BASE_URL | https://atlasiq-web-production.up.railway.app |

**Important**: Select all environments (Production, Preview, Development)

---

## ✅ After Deployment

Once Vercel deploys:

1. **Visit your Vercel URL** (e.g., https://atlasiq-web.vercel.app)
2. **Try to login**:
   - Email: `admin@atlasiq.com`
   - Password: `admin123`
3. **Check the dashboard** loads with data
4. **Share the URL** with others!

---

## 🐛 Troubleshooting

### Frontend can't connect to backend
- Check `VITE_API_BASE_URL` is set correctly in Vercel
- Make sure Railway backend is running (check https://atlasiq-web-production.up.railway.app/health)
- Check browser console for CORS errors

### Build fails on Vercel
- Check that `frontend/package.json` exists
- Verify build command includes `cd frontend`
- Check Vercel build logs for specific errors

### 404 on routes
- Vercel automatically handles SPA routing for Vite projects
- If issues persist, check `vercel.json` has rewrites configured

---

## 📝 Summary

**Backend (Railway)**:
- ✅ Deployed and running
- ✅ URL: https://atlasiq-web-production.up.railway.app
- ✅ Database initialized
- ✅ Admin account ready

**Frontend (Vercel)**:
- ⏳ Ready to deploy
- 🎯 Just add environment variable and deploy!

---

## 🎉 Next Steps

1. Deploy frontend to Vercel (use Option 1 or 2 above)
2. Test the complete application
3. Share the Vercel URL with others
4. Enjoy your deployed app! 🚀

