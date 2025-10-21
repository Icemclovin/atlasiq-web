# CORS Configuration Fix for Railway

## Problem
Login doesn't work on https://atlasiq-web.vercel.app because the backend (Railway) is blocking requests from the Vercel domain due to CORS restrictions.

## Solution
Add the Vercel domain to Railway's CORS_ORIGINS environment variable.

## Steps to Fix

### 1. Go to Railway Dashboard
- Visit: https://railway.app
- Login to your account
- Select your project: **atlasiq-web-production**

### 2. Add Environment Variable
1. Click on your backend service
2. Go to the **Variables** tab
3. Click **+ New Variable**
4. Add the following:

**Variable Name:**
```
CORS_ORIGINS
```

**Variable Value:**
```
http://localhost:3000,http://localhost:5173,https://atlasiq-web.vercel.app,https://atlasiq-web-git-main-icemclovins-projects.vercel.app,https://atlasiq-debxtcme5-icemclovins-projects.vercel.app,https://atlasiq-mfwats6mn-icemclovins-projects.vercel.app
```

**OR use wildcard for all Vercel preview deployments:**
```
http://localhost:3000,http://localhost:5173,https://atlasiq-web.vercel.app,https://*.vercel.app
```

5. Click **Add** or **Save**

### 3. Redeploy
Railway will automatically redeploy your backend with the new CORS settings. Wait about 1-2 minutes for the deployment to complete.

### 4. Test
1. Go to https://atlasiq-web.vercel.app
2. Try logging in with:
   - Email: `admin@atlasiq.com`
   - Password: `admin123`
3. Login should now work!

## What This Does
The CORS_ORIGINS variable tells the backend which domains are allowed to make requests to it. By adding your Vercel domains, the backend will accept login requests from your deployed frontend.

## Verification
After adding the variable and redeploying, you can verify CORS is working by:
1. Opening browser DevTools (F12)
2. Going to Console tab
3. Trying to login
4. You should NO LONGER see CORS errors like "blocked by CORS policy"

---

## Current Status
- ✅ Backend: https://atlasiq-web-production.up.railway.app (deployed)
- ✅ Frontend: https://atlasiq-web.vercel.app (deployed)
- ⏳ CORS: Needs Railway environment variable update
