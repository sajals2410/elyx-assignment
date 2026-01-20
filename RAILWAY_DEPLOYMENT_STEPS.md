# Railway Backend Deployment - Step by Step Guide

## Overview
This guide walks you through deploying your Flask backend to Railway and connecting it to your Vercel-hosted React frontend.

---

## Step 1: Create Railway Account & Project

1. **Go to Railway**
   - Visit: https://railway.app
   - Sign up or log in (you can use GitHub to sign in)

2. **Create New Project**
   - Click **"New Project"** button
   - Select **"Deploy from GitHub repo"**
   - Authorize Railway to access your GitHub account if prompted
   - Select your repository from the list

3. **Railway will automatically detect your project**
   - It should detect Python from your `requirements.txt` and `runtime.txt`
   - It will use your `Procfile` or `railway.json` for deployment configuration

---

## Step 2: Configure Environment Variables

1. **In Railway Dashboard:**
   - Click on your project
   - Go to the **"Variables"** tab (or click on your service → Variables)

2. **Add Environment Variable:**
   - Click **"New Variable"**
   - **Variable Name:** `GEMINI_API_KEY`
   - **Value:** `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
   - Click **"Add"**

3. **Optional - Add PORT variable (Railway sets this automatically, but you can add it):**
   - Railway automatically sets `PORT` environment variable
   - Your `api.py` already reads it: `port = int(os.getenv('PORT', 5001))`

---

## Step 3: Deploy & Get Railway URL

1. **Railway will automatically start deploying**
   - Watch the build logs in the Railway dashboard
   - Wait for deployment to complete (usually 2-5 minutes)

2. **Get Your Railway URL:**
   - Once deployed, Railway will generate a URL like: `https://your-project-name.up.railway.app`
   - Go to **"Settings"** → **"Networking"** or check the **"Deployments"** tab
   - Copy the generated URL (it will look like: `https://projectelyx-production.up.railway.app`)

3. **Test Your Backend:**
   - Visit: `https://your-railway-url.railway.app/api/health`
   - You should see: `{"status": "ok", "message": "Resource Allocator API is running"}`

---

## Step 4: Update Frontend to Use Railway URL

You have **TWO options** to connect your frontend to Railway:

### Option A: Set Environment Variable in Vercel (Recommended)

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com
   - Select your project

2. **Add Environment Variable:**
   - Go to **Settings** → **Environment Variables**
   - Click **"Add New"**
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://your-railway-url.railway.app/api`
     - Replace `your-railway-url` with your actual Railway URL
     - **Important:** Include `/api` at the end
   - Select environments: **Production**, **Preview**, and **Development** (or just Production)
   - Click **"Save"**

3. **Redeploy Frontend:**
   - Go to **Deployments** tab
   - Click the **"..."** menu on the latest deployment
   - Select **"Redeploy"**
   - Or push a new commit to trigger a redeploy

### Option B: Update Frontend Code Directly

1. **Edit `frontend/src/api.ts`:**
   - Open the file
   - Find line 8-11 where `API_BASE_URL` is defined
   - Replace `'https://your-api.railway.app/api'` with your actual Railway URL
   - Example: `'https://projectelyx-production.up.railway.app/api'`

2. **Commit and Push:**
   ```bash
   git add frontend/src/api.ts
   git commit -m "Update API URL to Railway backend"
   git push
   ```
   - Vercel will automatically redeploy

---

## Step 5: Verify Everything Works

1. **Test Backend Health:**
   - Visit: `https://your-railway-url.railway.app/api/health`
   - Should return: `{"status": "ok", ...}`

2. **Test Frontend Connection:**
   - Visit your Vercel frontend URL
   - Open browser DevTools (F12) → Console tab
   - The app should successfully connect to the Railway backend
   - Check for any CORS errors (there shouldn't be any)

3. **Test Full Flow:**
   - Try generating data in the frontend
   - Try generating a schedule
   - Verify everything works end-to-end

---

## Troubleshooting

### Backend Issues:

1. **Deployment Fails:**
   - Check Railway build logs for errors
   - Ensure `requirements.txt` has all dependencies
   - Verify `Procfile` or `railway.json` is correct

2. **Backend Not Responding:**
   - Check Railway logs: **Deployments** → Click deployment → **View Logs**
   - Verify `GEMINI_API_KEY` is set correctly
   - Check that port binding is correct (Railway sets PORT automatically)

3. **CORS Errors:**
   - The CORS configuration has been updated to allow all origins
   - If issues persist, check Railway logs for CORS-related errors

### Frontend Issues:

1. **Can't Connect to Backend:**
   - Verify `REACT_APP_API_URL` is set correctly in Vercel
   - Check that the URL includes `/api` at the end
   - Verify Railway backend is running (test `/api/health` endpoint)

2. **Environment Variable Not Working:**
   - Environment variables starting with `REACT_APP_` are required
   - Redeploy after adding environment variables
   - Check Vercel build logs to verify the variable is being used

---

## Quick Reference

### Railway URL Format:
```
https://your-project-name.up.railway.app
```

### API Endpoints:
- Health: `https://your-railway-url.railway.app/api/health`
- Generate Data: `POST /api/generate-data`
- Generate Schedule: `POST /api/generate-schedule`
- Get Schedule: `GET /api/schedule`
- Get Statistics: `GET /api/statistics`

### Environment Variables Needed:

**Railway:**
- `GEMINI_API_KEY` = `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
- `PORT` = (automatically set by Railway)

**Vercel:**
- `REACT_APP_API_URL` = `https://your-railway-url.railway.app/api`

---

## Summary Checklist

- [ ] Created Railway account
- [ ] Created new project from GitHub repo
- [ ] Added `GEMINI_API_KEY` environment variable
- [ ] Deployed backend successfully
- [ ] Got Railway URL
- [ ] Tested backend health endpoint
- [ ] Set `REACT_APP_API_URL` in Vercel (or updated `api.ts`)
- [ ] Redeployed frontend
- [ ] Tested full application flow
- [ ] Verified no CORS errors

---

## Next Steps

Once deployed:
- Monitor Railway logs for any errors
- Set up custom domain in Railway (optional)
- Consider adding monitoring/alerting
- Update CORS to restrict to your Vercel domain for better security
