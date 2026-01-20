# Backend Deployment Guide: Railway + Vercel Setup

## Overview

This project uses a **split deployment architecture**:
- **Frontend (React)**: Deployed on Vercel (static hosting)
- **Backend (Flask API)**: Deployed on Railway (Python runtime)

This separation is necessary because:
- Vercel excels at hosting static React apps but has limitations with Python backends
- Railway provides better support for Python/Flask applications with persistent file storage
- This architecture allows each service to use the best platform for its needs

---

## Part 1: Deploy Backend to Railway

### Step 1: Create Railway Account & Project

1. Go to [https://railway.app](https://railway.app)
2. Sign up/Login with your GitHub account
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository (`projectelyx`)

### Step 2: Configure Environment Variables

Railway needs the Gemini API key to generate data:

1. In your Railway project dashboard, go to **"Variables"** tab
2. Click **"New Variable"**
3. Add:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
4. Click **"Add"**

### Step 3: Configure Railway Service

Railway should auto-detect your Python app, but verify:

1. Go to **"Settings"** tab
2. Check **"Build Command"**: Should be empty (Railway auto-detects)
3. Check **"Start Command"**: Should be `python api.py` (already configured in `railway.json`)
4. Railway will automatically:
   - Install dependencies from `requirements.txt`
   - Run `python api.py` to start the Flask server

### Step 4: Get Your Railway URL

1. After deployment starts, go to **"Settings"** tab
2. Scroll to **"Networking"** section
3. Click **"Generate Domain"** (or use the auto-generated one)
4. Copy the URL (e.g., `https://your-project-name.up.railway.app`)
5. **Important**: Add `/api` to the end for API calls:
   - Full API URL: `https://your-project-name.up.railway.app/api`

### Step 5: Verify Backend is Running

Test your Railway backend:

```bash
# Replace with your Railway URL
curl https://your-project-name.up.railway.app/api/health
```

Expected response:
```json
{"status": "ok", "message": "Resource Allocator API is running"}
```

---

## Part 2: Connect Frontend to Railway Backend

You have **two options** to configure the frontend API URL:

### Option A: Update Frontend Code (Recommended for Testing)

Edit `frontend/src/api.ts`:

1. Open `frontend/src/api.ts`
2. Find line 10 (the production API URL)
3. Replace `https://your-api.railway.app/api` with your actual Railway URL:

```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://your-project-name.up.railway.app/api'  // Your Railway URL
    : 'http://localhost:5001/api');
```

4. Rebuild and redeploy frontend to Vercel

**Pros**: Simple, works immediately  
**Cons**: Requires code change and redeploy for URL changes

---

### Option B: Use Vercel Environment Variables (Recommended for Production)

This is the **better approach** for production because:
- No code changes needed
- Easy to update without redeploying
- Different URLs for different environments

#### Steps:

1. **In Vercel Dashboard**:
   - Go to your project: [https://vercel.com/dashboard](https://vercel.com/dashboard)
   - Select your `projectelyx` project
   - Go to **"Settings"** → **"Environment Variables"**

2. **Add Environment Variable**:
   - **Name**: `REACT_APP_API_URL`
   - **Value**: `https://your-project-name.up.railway.app/api` (your Railway URL)
   - **Environment**: Select all (Production, Preview, Development)
   - Click **"Save"**

3. **Redeploy Frontend**:
   - Go to **"Deployments"** tab
   - Click **"Redeploy"** on the latest deployment
   - Or push a new commit to trigger auto-deployment

4. **Verify**:
   - The frontend will now use `REACT_APP_API_URL` from environment variables
   - Check browser console to see the API URL being used

**Pros**: No code changes, flexible, production-ready  
**Cons**: Requires Vercel dashboard access

---

## Part 3: How It Works

### Current Configuration

The frontend (`frontend/src/api.ts`) uses this logic:

```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://your-api.railway.app/api'  // Fallback if env var not set
    : 'http://localhost:5001/api');       // Development mode
```

**Priority order**:
1. **First**: Checks `REACT_APP_API_URL` environment variable (set in Vercel)
2. **Second**: If in production and no env var, uses hardcoded Railway URL
3. **Third**: If in development, uses `localhost:5001`

### API Endpoints

Your Railway backend exposes these endpoints:
- `GET /api/health` - Health check
- `POST /api/generate-data` - Generate test data
- `POST /api/generate-schedule` - Generate schedule
- `GET /api/schedule` - Get current schedule
- `GET /api/statistics` - Get statistics
- `GET /api/download/<type>` - Download files
- `GET /api/activities` - Get activities list

---

## Part 4: Troubleshooting

### Backend Not Responding

1. **Check Railway Logs**:
   - Railway Dashboard → Your Service → "Deployments" → Click latest deployment → "View Logs"
   - Look for errors or startup issues

2. **Verify Environment Variables**:
   - Railway Dashboard → "Variables" tab
   - Ensure `GEMINI_API_KEY` is set correctly

3. **Test Health Endpoint**:
   ```bash
   curl https://your-railway-url.up.railway.app/api/health
   ```

### Frontend Can't Connect to Backend

1. **Check CORS**:
   - Backend already has CORS enabled for all origins (see `api.py` line 29-36)
   - Should work automatically

2. **Verify API URL**:
   - Open browser DevTools → Console
   - Look for API URL logs (only in development mode)
   - Check Network tab for failed requests

3. **Check Environment Variable**:
   - Vercel Dashboard → Settings → Environment Variables
   - Ensure `REACT_APP_API_URL` is set correctly
   - Must include `/api` at the end

4. **Redeploy Frontend**:
   - Environment variables require a redeploy to take effect
   - Vercel Dashboard → Deployments → Redeploy

### Common Issues

**Issue**: "Failed to fetch" error  
**Solution**: Check Railway URL is correct and includes `/api` suffix

**Issue**: CORS errors  
**Solution**: Backend already configured for CORS, but verify Railway URL matches exactly

**Issue**: 404 Not Found  
**Solution**: Ensure Railway URL ends with `/api` (e.g., `...railway.app/api`)

**Issue**: Environment variable not working  
**Solution**: 
- Variable name must start with `REACT_APP_` for React to access it
- Must redeploy after adding/changing environment variables

---

## Part 5: Quick Reference

### Railway Deployment Checklist

- [ ] Railway project created
- [ ] GitHub repo connected
- [ ] `GEMINI_API_KEY` environment variable added
- [ ] Railway URL generated and copied
- [ ] Health endpoint tested successfully

### Frontend Configuration Checklist

- [ ] Option A: Updated `frontend/src/api.ts` with Railway URL, OR
- [ ] Option B: Added `REACT_APP_API_URL` in Vercel environment variables
- [ ] Frontend redeployed
- [ ] Tested API connection from frontend

### Testing Commands

```bash
# Test Railway backend health
curl https://your-railway-url.up.railway.app/api/health

# Test from local frontend (development)
cd frontend && npm start
# Then check browser console for API calls

# Check Railway logs
# Railway Dashboard → Deployments → View Logs
```

---

## Summary

1. **Deploy backend to Railway**: Connect GitHub repo, add `GEMINI_API_KEY`, get Railway URL
2. **Configure frontend**: Either update `api.ts` or set `REACT_APP_API_URL` in Vercel
3. **Test**: Verify health endpoint and frontend-backend connection
4. **Deploy**: Frontend on Vercel automatically connects to Railway backend

Your app is now fully deployed with frontend on Vercel and backend on Railway! 🚀
