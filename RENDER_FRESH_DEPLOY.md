# 🚀 Deploy to Render - Step by Step (Fixed)

**Your Dockerfile is ready. Now let's deploy it to Render correctly.**

---

## ✅ What I Fixed

- ✅ Removed `render.yaml` (was confusing Render's auto-detection)
- ✅ Dockerfile uses Python 3.11-slim (stable)
- ✅ All dependencies compatible
- ✅ Code pushed to GitHub

---

## 📋 Step-by-Step Deployment

### Step 1: Go to Render Dashboard

1. Open **render.com** in your browser
2. Sign in to your account
3. Click **"Dashboard"** (top left)

---

### Step 2: Create New Web Service

1. Click **"New +"** button (top right)
2. Click **"Web Service"**

---

### Step 3: Connect Your Repository

1. Click **"Connect a repository"** button
2. Search for: **`foundathon`**
3. Select your **`saalini-t/foundathon`** repository
4. Click **"Connect"**

---

### Step 4: Configure the Service

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `foundathon-backend` |
| **Environment** | ⚠️ **IMPORTANT: Leave as default** (auto-detect will work) |
| **Branch** | `main` |
| **Build Command** | ⚠️ **Leave EMPTY** (Dockerfile will handle it) |
| **Start Command** | ⚠️ **Leave EMPTY** (Dockerfile will handle it) |
| **Plan** | `Free` (or paid if you want) |

---

### Step 5: Add Environment Variables

Click **"Advanced"** section, then scroll to **"Environment Variables"**

Add these variables:

| Key | Value |
|-----|-------|
| `FIRMS_API_KEY` | `2f2e12b87800276307048aad2c1fd52b` |
| `DATABASE_URL` | `sqlite:///./data/ecosystem_monitor.db` |
| `DEBUG` | `false` |
| `FRONTEND_URL` | *Leave empty for now* |

---

### Step 6: Deploy

1. Click **"Create Web Service"** button
2. Wait for deployment to start
3. Render should **auto-detect the Dockerfile**

---

## 📊 What to Watch For

### Success Signs (Look in Logs):

```
✅ Building Docker image...
✅ FROM python:3.11-slim
✅ Running pip install...
✅ Successfully built foundathon-backend
✅ Listening on 0.0.0.0:8000
✅ Application startup complete
```

### If It Still Fails:

If you still see Python 3.14, it means Render didn't detect the Dockerfile.

**Workaround**: Contact Render support or try Railway instead (easier Docker support).

---

## ✅ When Deployment Completes

You'll get a URL like: `https://foundathon-backend.onrender.com`

### Test It:

```bash
# Should return {"status":"healthy"}
curl https://foundathon-backend.onrender.com/health

# Should return ecosystem data
curl https://foundathon-backend.onrender.com/api/regions
```

---

## 🎯 After Backend Deploys Successfully

### Update Frontend's API URL

1. Go to **vercel.com** → Dashboard
2. Click **`foundathon-frontend`** project
3. **Settings** → **Environment Variables**
4. Update `VITE_API_URL`:
   ```
   https://foundathon-backend.onrender.com
   ```
5. Click **"Save"** → Vercel auto-redeploys

### Update Backend's Frontend URL

1. Go to **render.com** → Dashboard
2. Click **`foundathon-backend`** service
3. **Environment** tab
4. Add/update `FRONTEND_URL`:
   ```
   https://foundathon-frontend.vercel.app
   ```
5. Click **"Save"** → Backend auto-redeploys

---

## ⏱️ Timeline

| Step | Time |
|------|------|
| Configure service | 2 min |
| Build Docker image | 3-5 min |
| Deploy & start | 2 min |
| Update environment vars | 2 min |
| **Total** | **~10 minutes** |

---

## 🆘 If Docker Still Doesn't Work

If Render keeps using Python 3.14 and not detecting Dockerfile:

**Option A: Try Railway Instead**
```bash
# Much better Docker support on Railway
# Follow: RENDER_VERCEL_DEPLOYMENT.md → Railway section
```

**Option B: Contact Render Support**
- Email: support@render.com
- Issue: "Docker runtime not being detected, still using Python 3.14"

**Option C: Deploy Backend Differently**
- Use Railway (better Docker support)
- Or AWS EC2 (manual setup but full control)

---

## Summary

✅ **Dockerfile is ready** (Python 3.11)
✅ **Code on GitHub** (commit f353850)
✅ **Frontend on Vercel** (already live)
⏳ **Backend on Render** (create service following steps above)

**Just follow the steps above and you're done!** 🚀
