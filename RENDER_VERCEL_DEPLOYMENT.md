# 🚀 PRODUCTION DEPLOYMENT GUIDE - Vercel + Render

**Your Ecosystem & Biodiversity Monitor is ready for production deployment!**

This guide will walk you through deploying:
- **Frontend**: Vercel (free, global CDN, optimized for React)
- **Backend**: Render (full app, auto-deploy on push)

**Total time: ~30 minutes**

---

## Prerequisites ✅

Before starting, make sure you have:
- [ ] GitHub account (free at github.com)
- [ ] Vercel account (free at vercel.com)
- [ ] Render account (free at render.com)
- [ ] Git installed locally
- [ ] Your project code ready

---

## Step 1: Initialize Git Repository

```bash
cd c:\Saalu_Data\foundathon

# Initialize git (if not already done)
git init

# Add all files
git add .

# Initial commit
git commit -m "Initial commit: Ecosystem Monitor production ready"

# Show git status
git status
```

Expected output:
```
On branch master
nothing to commit, working tree clean
```

---

## Step 2: Push Code to GitHub

### 2A. Create GitHub Repository

1. Go to github.com and sign in
2. Click **"+"** → **"New repository"**
3. Fill in:
   - **Repository name**: `foundathon`
   - **Description**: "AI-Powered Ecosystem & Biodiversity Monitoring Platform"
   - **Visibility**: Public (for free tier) or Private (if you have pro)
   - **Do NOT** initialize with README (you already have one)
4. Click **"Create repository"**

### 2B. Connect Local Git to GitHub

Copy the commands from GitHub (they'll look like this):

```bash
cd c:\Saalu_Data\foundathon

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/foundathon.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 3: Deploy Backend to Render

### 3A. Create New Web Service on Render

1. Go to render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Search for and select your **`foundathon`** repository
5. Click **"Connect"**

### 3B. Configure Render Service

Fill in the following:

| Field | Value |
|-------|-------|
| **Name** | `foundathon-backend` |
| **Environment** | `Python 3` |
| **Region** | `Oregon` (or your preferred region) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT` |
| **Plan** | `Free` (or paid if you need) |

### 3C. Add Environment Variables

Click **"Advanced"** and add these environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `FIRMS_API_KEY` | `2f2e12b87800276307048aad2c1fd52b` | NASA API key |
| `DATABASE_URL` | `sqlite:///./data/ecosystem_monitor.db` | SQLite path |
| `DEBUG` | `false` | Production mode |
| `HOST` | `0.0.0.0` | Listen on all interfaces |
| `FRONTEND_URL` | *See below* | Will get from Vercel |

**For `FRONTEND_URL`**: Leave this for now, you'll update it after deploying frontend to get the Vercel URL.

### 3D. Deploy

Click **"Create Web Service"**

Render will automatically:
- ✅ Clone your repository
- ✅ Install Python dependencies
- ✅ Start the backend service
- ✅ Give you a URL like `https://foundathon-backend.onrender.com`

**⏱️ First deployment takes ~5-10 minutes. Wait for "Live" status.**

**Save your Render backend URL!** You'll need it in the next step.

---

## Step 4: Deploy Frontend to Vercel

### 4A. Create New Project on Vercel

1. Go to vercel.com and sign in
2. Click **"Add New +"** → **"Project"**
3. Click **"Continue with GitHub"** (authorize if needed)
4. Search for your **`foundathon`** repository
5. Click **"Import"**

### 4B: Configure Vercel Project

Fill in the following:

| Field | Value |
|-------|-------|
| **Project Name** | `foundathon-frontend` |
| **Framework Preset** | `Vite` |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

### 4C: Add Environment Variables

In the **"Environment Variables"** section, add:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://foundathon-backend.onrender.com` |

Replace with your actual **Render backend URL**!

### 4D: Deploy

Click **"Deploy"**

Vercel will automatically:
- ✅ Clone your repository
- ✅ Install dependencies
- ✅ Build frontend
- ✅ Deploy to global CDN
- ✅ Give you a URL like `https://foundathon-frontend.vercel.app`

**✅ Your frontend is now live!**

---

## Step 5: Update Backend FRONTEND_URL

Now that you have your Vercel URL, update the backend:

### 5A: On Render Dashboard

1. Go to render.com dashboard
2. Click on **`foundathon-backend`** service
3. Go to **"Environment"**
4. Edit **`FRONTEND_URL`**
5. Set it to: `https://YOUR_VERCEL_URL.vercel.app`
6. Click **"Save"** (backend will redeploy automatically)

### 5B: Verify CORS Works

Wait ~2 minutes for redeploy, then:

```bash
# Test API from your Vercel frontend URL
curl -H "Origin: https://foundathon-frontend.vercel.app" \
  https://foundathon-backend.onrender.com/api/regions \
  -v
```

You should see:
```
Access-Control-Allow-Origin: https://foundathon-frontend.vercel.app
```

---

## Step 6: Verify Deployment

### 6A: Test Backend

```bash
# Health check
curl https://foundathon-backend.onrender.com/health

# API endpoints
curl https://foundathon-backend.onrender.com/api/regions
curl https://foundathon-backend.onrender.com/api/predict/ehi?region=western_ghats
curl https://foundathon-backend.onrender.com/api/narrative/8.05_76.05?region=western_ghats
```

Expected: **200 OK** responses with JSON data

### 6B: Test Frontend

1. Open: `https://foundathon-frontend.vercel.app`
2. Should see:
   - ✅ Map loads (might show "Loading layer data...")
   - ✅ Header with stats (Fire Alerts, Species, etc.)
   - ✅ Region selector (Western Ghats, Amazon, etc.)
3. Click on a grid cell
4. Should see AI Ecosystem Summary in sidebar

### 6C: Test AI Narrative

```bash
# Should return ecosystem summary
curl https://foundathon-backend.onrender.com/api/narrative/8.05_76.05?region=western_ghats | python -m json.tool
```

Expected response:
```json
{
  "cell_id": "8.05_76.05",
  "narrative": "Overall ecosystem health scores **64/100** (good)...",
  "data": {...}
}
```

---

## Step 7: Future Updates (Auto Deploy)

Your setup now has **automatic deployment on push**:

### To Update Backend or Frontend:

```bash
cd c:\Saalu_Data\foundathon

# Make changes to code

git add .
git commit -m "Fix: your message here"
git push origin main
```

**That's it!** Both services will automatically redeploy within 1-2 minutes.

You can watch the deployment in:
- **Render Dashboard** → Logs tab
- **Vercel Dashboard** → Deployments tab

---

## Troubleshooting

### Issue: Frontend shows "API Error" or "Loading..."

**Fix:**
1. Check browser console (F12) for errors
2. Verify `VITE_API_URL` environment variable in Vercel
3. Check that Render backend is running (not in "Suspended" state)
4. Render free tier sleeps after 15 min of inactivity — click a link to wake it

### Issue: Vercel shows "Build failed"

**Fix:**
1. Check Vercel "Deployments" → "Logs" tab
2. Common causes:
   - `frontend/` not in root directory
   - Missing `package.json` in `frontend/`
   - npm install fails (check npm version)

### Issue: Render shows "Build failed"

**Fix:**
1. Check Render "Logs" tab
2. Common causes:
   - Missing `requirements.txt`
   - `gunicorn` not installed
   - Python version incompatibility

### Issue: CORS errors in browser

**Fix:**
1. Update `FRONTEND_URL` in Render environment
2. Make sure it matches your Vercel URL exactly
3. Redeploy Render backend

### Issue: Map doesn't show but header shows stats

**Fix:**
1. Verify API response: `curl https://your-backend/api/predict/ehi`
2. Check browser console for fetch errors
3. Verify GeoJSON is valid JSON (not HTML error page)

---

## Performance Tips

### For Better Performance:

**Backend (Render):**
- Use paid plan if you expect traffic (free plan has limited memory/CPU)
- Enable HTTP/2 (automatic on Render)
- Use PostgreSQL instead of SQLite for production (see `.env`)

**Frontend (Vercel):**
- Already optimized with global CDN
- Build is minified automatically
- Caching handled automatically

---

## Monitoring & Logs

### View Backend Logs (Render)

1. Go to render.com dashboard
2. Click **`foundathon-backend`**
3. Click **"Logs"** tab
4. See real-time logs

### View Frontend Logs (Vercel)

1. Go to vercel.com dashboard
2. Click **`foundathon-frontend`**
3. Click **"Deployments"** tab
4. Click latest deployment → "Logs"

---

## Production Checklist

- [ ] Backend deployed on Render
- [ ] Frontend deployed on Vercel
- [ ] `FRONTEND_URL` updated in Render
- [ ] `VITE_API_URL` configured in Vercel
- [ ] API endpoints responding (200 OK)
- [ ] Frontend loads without errors
- [ ] Map renders
- [ ] Grid cells clickable
- [ ] AI summary appears on click
- [ ] All 6 layers toggle correctly
- [ ] Fire alerts showing
- [ ] Statistics dashboard working

---

## Next Steps

### Optional: Custom Domain

To use your own domain (e.g., `ecosystem.yourcompany.com`):

**For Vercel Frontend:**
1. Go to Vercel dashboard
2. Project settings → Domains
3. Add your custom domain
4. Update DNS records (Vercel will give instructions)

**For Render Backend:**
1. Go to Render dashboard
2. Service settings → Custom domains
3. Add your custom domain
4. Update DNS records

### Optional: SSL Certificate

- Vercel: **Automatic** (free Let's Encrypt)
- Render: **Automatic** (free Let's Encrypt)

Both handle SSL/TLS automatically! ✅

---

## Summary

**You now have:**

✅ **Frontend deployed** on Vercel (global CDN, instant updates)
✅ **Backend deployed** on Render (auto-restart, health checks)
✅ **Automatic deployments** on git push
✅ **CORS configured** for secure cross-domain requests
✅ **All features working**: maps, AI summaries, real-time data

**Time to deployment: ~30 minutes** ⏱️

---

## Support

**If you get stuck:**

1. Check the "Troubleshooting" section above
2. Review logs on Render/Vercel dashboards
3. Test endpoints manually with curl
4. Check GitHub issues for similar problems

**You're live! 🎉**

---

Last Updated: May 15, 2026
