# Railway Deployment - Next Steps

## ✅ What We Just Fixed

- Fixed dependency conflict (redis version)
- Created minimal `requirements.prod.txt` for faster deployments
- Updated Dockerfile to use production requirements
- Pushed fixes to GitHub

## 🚀 Current Status

Railway is now automatically redeploying with the fixed dependencies.

---

## 📋 Step-by-Step Instructions

### Step 1: Check Deployment Status

1. Go to your Railway dashboard: https://railway.app/
2. Click on your **atlasiq-web** project
3. Click on the **backend service**
4. Go to the **Deployments** tab
5. Watch the latest deployment logs

**What to look for:**
- ✅ "Using Detected Dockerfile"
- ✅ "Successfully installed fastapi, uvicorn, sqlalchemy..." (should take ~1-2 minutes)
- ✅ "Deployment successful"

**If you see errors**, copy the error message and I'll help fix it.

---

### Step 2: Generate Public Domain (After Successful Deployment)

1. In Railway, click on your **backend service**
2. Go to the **Settings** tab
3. Scroll down to **Networking** section
4. Click **Generate Domain** button
5. Railway will create a URL like: `https://atlasiq-web-production-xxx.up.railway.app`
6. **COPY THIS URL** - you'll need it for the frontend!

---

### Step 3: Test Your Backend

Once you have the domain:

1. Open a browser
2. Visit: `https://YOUR-RAILWAY-URL.up.railway.app/health`
3. You should see: `{"status":"healthy"}`

Also test the docs:
- Visit: `https://YOUR-RAILWAY-URL.up.railway.app/docs`
- You should see the interactive API documentation

---

### Step 4: Add Environment Variables (Important!)

1. In Railway, go to **Variables** tab
2. Add these variables:

```
DATABASE_URL=sqlite+aiosqlite:///./data/atlasiq.db
JWT_SECRET_KEY=<generate-random-32-char-string>
JWT_ALGORITHM=HS256
DEBUG=false
CORS_ORIGINS=["*"]
APP_ENV=production
```

**To generate a secure JWT_SECRET_KEY**, run in PowerShell:
```powershell
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

3. Click **Save** - Railway will automatically redeploy

---

### Step 5: Create Admin Account on Railway

After the backend is live, we need to create an admin account in the production database.

**Option A: Use Railway CLI (Recommended)**
```bash
railway login
railway link
railway run python create_account.py
```

**Option B: Modify create_account.py to use Railway URL**
I can help you create a script that creates an account via the API.

---

### Step 6: Deploy Frontend to Vercel

Once backend is working:

1. Go to https://vercel.com/
2. Sign in with GitHub
3. Click **Add New Project**
4. Import your **atlasiq-web** repository
5. Configure:
   - **Root Directory**: `frontend`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add **Environment Variable**:
   - **Name**: `VITE_API_BASE_URL`
   - **Value**: `https://YOUR-RAILWAY-URL.up.railway.app`
7. Click **Deploy**

Vercel will build and deploy (takes ~1-2 minutes).

---

### Step 7: Test Complete Application

1. Visit your Vercel URL (e.g., `https://atlasiq-web.vercel.app`)
2. Try to login with: `admin@atlasiq.com` / `admin123`
3. Verify dashboard loads with data
4. Test navigation and features

---

### Step 8: Share Your App! 🎉

Once everything works:
- **Frontend URL**: Your Vercel URL (e.g., `https://atlasiq-web.vercel.app`)
- **Backend URL**: Your Railway URL (for API access)

Share the frontend URL with anyone you want to access the app!

---

## 🐛 Troubleshooting

### Backend won't start
- Check Railway logs for errors
- Verify all environment variables are set
- Make sure DATABASE_URL uses `sqlite+aiosqlite://`

### Frontend can't connect to backend
- Check CORS settings in backend
- Verify VITE_API_BASE_URL is correct
- Make sure Railway domain is generated and accessible

### Login doesn't work
- Create admin account on production database
- Check JWT_SECRET_KEY is set
- Verify backend /api/v1/auth/login endpoint works in /docs

---

## 📞 Need Help?

If you encounter any errors:
1. Copy the exact error message
2. Take a screenshot of the logs
3. Tell me which step you're on
4. I'll help you fix it!

---

## 🎯 Current Step

**YOU ARE HERE**: Waiting for Railway deployment to complete

**NEXT**: Check deployment logs, then generate domain

