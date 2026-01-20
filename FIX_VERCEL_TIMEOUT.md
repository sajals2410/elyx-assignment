# 🔧 Fix Vercel Timeout Issue

## Problem
Vercel Python serverless functions are timing out. This is a known limitation of Vercel's Python runtime.

## ✅ Solution: Deploy Backend to Railway

### Step 1: Push Code to GitHub

```bash
cd /Users/sajalsingh/Desktop/projectelyx
git add .
git commit -m "Prepare for Railway backend deployment"
git push origin main
```

### Step 2: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** (use GitHub - easiest)
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your repository**: `elyx-assignment` (or your repo name)
6. **Railway will automatically:**
   - Detect Python
   - Install dependencies from `requirements.txt`
   - Start the Flask API

7. **Add Environment Variable:**
   - Click on your service
   - Go to **Variables** tab
   - Click **+ New Variable**
   - Name: `GEMINI_API_KEY`
   - Value: `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
   - Click **Add**

8. **Get Your API URL:**
   - Go to **Settings** tab
   - Click **Generate Domain** (or use existing)
   - Copy the URL (e.g., `https://projectelyx-production.up.railway.app`)
   - **SAVE THIS URL!**

### Step 3: Update Frontend API URL

**Edit `frontend/src/api.ts`:**

Find this line (around line 8):
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://your-api.railway.app/api'  // Update with your Railway URL
    : 'http://localhost:5001/api');
```

**Replace `your-api.railway.app` with your actual Railway URL:**

Example:
```typescript
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://projectelyx-production.up.railway.app/api'
    : 'http://localhost:5001/api');
```

### Step 4: Commit and Push Frontend Change

```bash
git add frontend/src/api.ts
git commit -m "Update API URL to Railway backend"
git push origin main
```

### Step 5: Redeploy Frontend to Vercel

```bash
npx vercel --prod
```

Or if already linked:
- Go to Vercel Dashboard
- Your project → Deployments
- Click "Redeploy" on latest deployment

---

## ✅ Test After Deployment

1. **Test Railway Backend:**
   ```bash
   curl https://your-api.railway.app/api/health
   ```
   Should return: `{"status":"ok","message":"Resource Allocator API is running"}`

2. **Test Frontend:**
   - Open: `https://projectelyx.vercel.app`
   - Check API status (should be green ✅)
   - Generate a schedule
   - Verify it works!

---

## 🎯 Final Architecture

```
User Browser
    │
    ▼
React Frontend (Vercel)
    │
    │ API Calls
    ▼
Flask API (Railway) ✅
```

---

## ⚠️ Why Railway Instead of Vercel?

- ✅ **No timeout issues** - Railway runs full Flask app
- ✅ **Better for Python** - Designed for long-running processes
- ✅ **Free tier** - $5 credit/month (more than enough)
- ✅ **Easier debugging** - Full logs and console access
- ✅ **More reliable** - No cold start delays

---

## 🆘 Troubleshooting

**Railway Issues:**
- Check Railway logs: Dashboard → Service → Logs
- Verify `requirements.txt` is correct
- Check that `api.py` exists in root
- Verify `GEMINI_API_KEY` is set

**Vercel Issues:**
- Frontend should work fine (it's just static React)
- If frontend doesn't load, check Vercel build logs

**CORS Issues:**
- Already handled in `api.py` with `CORS(app)`
- Should work automatically

---

**This is the recommended solution! Railway + Vercel works perfectly.** 🚀
