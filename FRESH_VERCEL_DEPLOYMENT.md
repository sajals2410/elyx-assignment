# 🚀 Fresh Vercel Deployment Guide

## Overview

This guide sets up a **fresh Vercel deployment** with:
- ✅ **Frontend**: React app on Vercel (static hosting - fast & reliable)
- ✅ **Backend**: Flask API on Railway (to avoid timeout issues)

---

## Step 1: Prepare Frontend for Vercel

The frontend is already configured. Vercel will:
- Auto-detect React
- Run `npm install` and `npm run build`
- Serve static files from `frontend/build`

---

## Step 2: Deploy Frontend to Vercel

### Option A: Using Vercel CLI (Recommended)

```bash
cd /Users/sajalsingh/Desktop/projectelyx

# Install Vercel CLI (if not already installed)
npm install -g vercel

# Login to Vercel
vercel login

# Deploy (from project root)
vercel

# Follow prompts:
# - Set up and deploy? Yes
# - Which scope? (Your account)
# - Link to existing project? No
# - Project name? projectelyx (or your choice)
# - Directory? frontend
# - Override settings? No

# Deploy to production
vercel --prod
```

### Option B: Using Vercel Dashboard

1. **Go to**: https://vercel.com
2. **Sign up/Login** (use GitHub - easiest)
3. **Click "Add New Project"**
4. **Import Git Repository**:
   - Select your GitHub repository
   - Click "Import"
5. **Configure Project**:
   - **Framework Preset**: Create React App (auto-detected)
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `build` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)
6. **Environment Variables** (optional for now):
   - We'll add `REACT_APP_API_URL` after Railway deployment
7. **Click "Deploy"**

---

## Step 3: Deploy Backend to Railway

Since Vercel Python functions have timeout issues, deploy backend separately:

1. **Go to**: https://railway.app
2. **New Project** → **Deploy from GitHub repo**
3. **Select your repository**
4. **Railway will auto-detect** Python/Flask
5. **Add Environment Variable**:
   - Name: `GEMINI_API_KEY`
   - Value: `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
6. **Get Railway URL** (e.g., `https://projectelyx-production.up.railway.app`)

---

## Step 4: Connect Frontend to Backend

### Update Frontend API URL

**Option A: Update Code**
Edit `frontend/src/api.ts`:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://your-railway-url.railway.app/api'
    : 'http://localhost:5001/api');
```

Replace `your-railway-url.railway.app` with your actual Railway URL.

**Option B: Use Environment Variable (Better)**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://your-railway-url.railway.app/api`
   - **Environments**: Production, Preview, Development
3. **Save**
4. **Redeploy**: Vercel Dashboard → Deployments → Redeploy

---

## Step 5: Commit and Push Changes

```bash
cd /Users/sajalsingh/Desktop/projectelyx

# Update frontend API URL (if using Option A)
# Edit frontend/src/api.ts with Railway URL

git add .
git commit -m "Configure for Vercel frontend + Railway backend"
git push origin main
```

---

## Step 6: Redeploy

### Frontend (Vercel)
- If using CLI: `vercel --prod`
- If using Dashboard: Click "Redeploy" on latest deployment

### Backend (Railway)
- Auto-deploys on git push (if connected to GitHub)
- Or manually trigger from Railway dashboard

---

## ✅ Final Architecture

```
User Browser
    │
    ▼
React Frontend (Vercel)
    │
    │ API Calls
    ▼
Flask API (Railway)
```

---

## 🧪 Testing

1. **Test Frontend**: Open `https://your-project.vercel.app`
2. **Test Backend**: `curl https://your-railway-url.railway.app/api/health`
3. **Test Integration**: Generate a schedule in the frontend

---

## 🆘 Troubleshooting

### Frontend Issues
- **Build fails**: Check Vercel build logs
- **404 errors**: Verify `vercel.json` routes are correct
- **API not connecting**: Check `REACT_APP_API_URL` env var

### Backend Issues
- **Timeout**: Railway should not timeout (unlike Vercel)
- **CORS errors**: Already handled in `api.py`
- **API not responding**: Check Railway logs

---

## 📋 Quick Commands

```bash
# Deploy to Vercel
vercel --prod

# Check deployment status
vercel ls

# View logs
vercel logs

# Update environment variables
# (Use Vercel Dashboard → Settings → Environment Variables)
```

---

**This setup avoids Vercel timeout issues by using Railway for the backend!** 🚀
