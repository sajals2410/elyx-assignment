# Troubleshooting "Failed to fetch" Error

## What is "Failed to fetch"?

This error occurs when the frontend cannot connect to the backend API. It's a network-level error that happens before any HTTP response is received.

## Common Causes & Solutions

### 1. **Backend Not Running (Local Development)**

**Symptoms:**
- Error: "Failed to fetch"
- API status shows: 🔴 API Disconnected
- Console shows: "Cannot connect to backend at http://localhost:5001/api"

**Solution:**
```bash
# Start the Flask backend
cd /Users/sajalsingh/Desktop/projectelyx
python api.py

# Or use the start script
./start_api.sh
```

**Verify:**
- Visit `http://localhost:5001/api/health` in your browser
- Should return: `{"status": "ok", "message": "Resource Allocator API is running"}`

---

### 2. **Wrong API URL (Production/Vercel)**

**Symptoms:**
- Error: "Failed to fetch"
- API URL shows placeholder: `https://your-api.railway.app/api`
- App is deployed on Vercel but backend isn't configured

**Solution:**

**Option A: Set Environment Variable in Vercel (Recommended)**
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add new variable:
   - **Name:** `REACT_APP_API_URL`
   - **Value:** `https://your-actual-railway-url.railway.app/api`
   - Replace with your actual Railway URL
3. Redeploy the frontend

**Option B: Update Code Directly**
1. Edit `frontend/src/api.ts`
2. Replace line 10:
   ```typescript
   ? 'https://your-actual-railway-url.railway.app/api'
   ```
3. Commit and push (Vercel will auto-deploy)

---

### 3. **Railway Backend Not Deployed**

**Symptoms:**
- Railway URL returns 404 or connection refused
- Health check fails

**Solution:**
1. Go to Railway Dashboard
2. Check deployment status
3. Verify environment variable `GEMINI_API_KEY` is set
4. Check Railway logs for errors
5. Ensure `Procfile` or `railway.json` is correct

**Test Railway Backend:**
```bash
# Replace with your Railway URL
curl https://your-project.up.railway.app/api/health
```

---

### 4. **CORS Issues**

**Symptoms:**
- Error in console: "CORS policy: No 'Access-Control-Allow-Origin' header"
- Backend responds but browser blocks it

**Solution:**
- CORS is already configured in `api.py` to allow all origins
- If issues persist, check Railway logs
- Verify `flask-cors` is in `requirements.txt`

---

### 5. **Network/Firewall Issues**

**Symptoms:**
- Works locally but not in production
- Intermittent failures

**Solution:**
- Check if Railway URL is accessible: `curl https://your-railway-url.railway.app/api/health`
- Verify no firewall blocking requests
- Check Railway service status

---

## Diagnostic Steps

### Step 1: Check Current API URL

Open browser console (F12) and look for:
```
API Base URL: http://localhost:5001/api
```
or
```
API Base URL: https://your-api.railway.app/api
```

### Step 2: Test Backend Directly

**Local:**
```bash
curl http://localhost:5001/api/health
```

**Production (Railway):**
```bash
curl https://your-railway-url.railway.app/api/health
```

Expected response:
```json
{"status": "ok", "message": "Resource Allocator API is running"}
```

### Step 3: Check Browser Network Tab

1. Open DevTools (F12) → Network tab
2. Try to use the app
3. Look for failed requests
4. Check:
   - Request URL (is it correct?)
   - Status code (404, 500, etc.)
   - Error message

### Step 4: Check Console Logs

Look for:
- `Health check: Connecting to [URL]`
- `Health check response status: [status]`
- Any CORS errors
- Network errors

---

## Quick Fixes

### For Local Development:
```bash
# Terminal 1: Start backend
cd /Users/sajalsingh/Desktop/projectelyx
python api.py

# Terminal 2: Start frontend
cd frontend
npm start
```

### For Production:
1. **Get Railway URL:**
   - Railway Dashboard → Your Project → Settings → Networking
   - Copy the URL (e.g., `https://projectelyx-production.up.railway.app`)

2. **Set in Vercel:**
   - Vercel Dashboard → Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = `https://your-railway-url.railway.app/api`

3. **Redeploy:**
   - Vercel Dashboard → Deployments → Redeploy

---

## Environment Variable Checklist

### Local Development:
- No environment variable needed (defaults to `http://localhost:5001/api`)

### Production (Vercel):
- ✅ `REACT_APP_API_URL` = `https://your-railway-url.railway.app/api`

### Railway Backend:
- ✅ `GEMINI_API_KEY` = `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
- ✅ `PORT` = (automatically set by Railway)

---

## Still Having Issues?

1. **Check Railway Logs:**
   - Railway Dashboard → Deployments → View Logs
   - Look for Python errors, import errors, etc.

2. **Check Vercel Logs:**
   - Vercel Dashboard → Deployments → View Logs
   - Look for build errors

3. **Verify Files:**
   - `api.py` exists and is correct
   - `requirements.txt` has all dependencies
   - `Procfile` or `railway.json` is correct

4. **Test API Endpoints:**
   ```bash
   # Health check
   curl https://your-railway-url.railway.app/api/health
   
   # Generate data (POST)
   curl -X POST https://your-railway-url.railway.app/api/generate-data \
     -H "Content-Type: application/json" \
     -d '{"start_date": "2026-01-15", "duration_months": 3, "use_gemini": true}'
   ```

---

## Summary

The "Failed to fetch" error means the frontend cannot reach the backend. Most common causes:

1. ✅ Backend not running (local)
2. ✅ Wrong API URL (production)
3. ✅ Railway backend not deployed
4. ✅ CORS configuration
5. ✅ Network/firewall issues

Follow the diagnostic steps above to identify and fix the issue!
