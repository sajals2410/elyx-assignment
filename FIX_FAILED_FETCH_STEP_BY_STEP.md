# Step-by-Step Fix for "Failed to fetch" Error

## 🔍 Step 1: Identify Your Situation

**Are you running locally or is this deployed on Vercel?**

- **Local Development** → Go to Step 2A
- **Deployed on Vercel** → Go to Step 2B

---

## 🖥️ Step 2A: Fix for Local Development

### Check if Backend is Running

1. **Open a terminal and check:**
   ```bash
   curl http://localhost:5001/api/health
   ```

2. **If you get an error or no response:**
   - The backend is NOT running
   - Continue to Step 3A

3. **If you see:** `{"status": "ok", "message": "Resource Allocator API is running"}`
   - Backend is running ✅
   - The issue might be CORS or frontend configuration
   - Go to Step 4A

---

### Step 3A: Start the Backend

**Option 1: Simple Start (Recommended)**
```bash
cd /Users/sajalsingh/Desktop/projectelyx
python api.py
```

You should see:
```
 * Running on http://0.0.0.0:5001
```

**Option 2: Using Virtual Environment**
```bash
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate
python api.py
```

**Option 3: Using the Start Script**
```bash
cd /Users/sajalsingh/Desktop/projectelyx
./start_api.sh
```

**Keep this terminal open!** The backend must stay running.

---

### Step 4A: Verify Backend is Working

1. **Open a new terminal** (keep the backend running in the first one)

2. **Test the backend:**
   ```bash
   curl http://localhost:5001/api/health
   ```

3. **Expected response:**
   ```json
   {"status": "ok", "message": "Resource Allocator API is running"}
   ```

4. **If this works:** ✅ Backend is running correctly
5. **If this fails:** Check for errors in the backend terminal

---

### Step 5A: Start the Frontend

1. **Open a new terminal** (keep backend running)

2. **Start React:**
   ```bash
   cd /Users/sajalsingh/Desktop/projectelyx/frontend
   npm start
   ```

3. **Wait for it to open** in your browser at `http://localhost:3000`

4. **Check the browser console** (F12 → Console tab):
   - Look for: `API Base URL: http://localhost:5001/api`
   - If you see this, the frontend is configured correctly ✅

---

### Step 6A: Test the Connection

1. **In your browser** (at http://localhost:3000):
   - Look at the top of the page
   - Should show: **🟢 API Connected** (green)
   - If it shows **🔴 API Disconnected** (red), continue troubleshooting

2. **Open Browser DevTools** (F12):
   - Go to **Console** tab
   - Look for error messages
   - Go to **Network** tab
   - Try using the app
   - Look for failed requests (they'll be red)

---

### Step 7A: Common Local Issues

**Issue: Port 5001 is already in use**
```bash
# Find what's using port 5001
lsof -ti:5001

# Kill the process (replace PID with actual process ID)
kill -9 <PID>

# Or use a different port
PORT=5002 python api.py
```

**Issue: CORS errors in console**
- The CORS is already configured to allow all origins
- If you still see CORS errors, check that `flask-cors` is installed:
  ```bash
  pip install flask-cors
  ```

**Issue: Frontend can't find backend**
- Make sure both are running
- Check that API URL in console shows: `http://localhost:5001/api`
- Try refreshing the browser

---

## 🌐 Step 2B: Fix for Production (Vercel Deployment)

### Step 1B: Get Your Railway Backend URL

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app
   - Log in and select your project

2. **Find your service URL:**
   - Click on your service
   - Go to **Settings** → **Networking**
   - Or check the **Deployments** tab
   - Copy the URL (e.g., `https://projectelyx-production.up.railway.app`)

3. **Test your Railway backend:**
   ```bash
   curl https://your-railway-url.railway.app/api/health
   ```
   Should return: `{"status": "ok", ...}`

---

### Step 2B: Set Environment Variable in Vercel

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com
   - Select your project

2. **Navigate to Environment Variables:**
   - Click **Settings** (in the top menu)
   - Click **Environment Variables** (in the left sidebar)

3. **Add the API URL:**
   - Click **Add New**
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://your-railway-url.railway.app/api`
     - ⚠️ **Important:** Replace `your-railway-url` with your actual Railway URL
     - ⚠️ **Important:** Include `/api` at the end!
   - **Environments:** Select all (Production, Preview, Development)
   - Click **Save**

4. **Verify it was added:**
   - You should see `REACT_APP_API_URL` in the list
   - The value should be your Railway URL with `/api` at the end

---

### Step 3B: Redeploy Frontend

1. **In Vercel Dashboard:**
   - Go to **Deployments** tab
   - Find your latest deployment
   - Click the **"..."** menu (three dots)
   - Select **"Redeploy"**
   - Confirm the redeploy

2. **Wait for deployment to complete** (usually 1-2 minutes)

3. **Or trigger a new deployment:**
   ```bash
   # Make a small change and commit
   git add .
   git commit -m "Trigger redeploy"
   git push
   ```

---

### Step 4B: Verify It's Working

1. **Visit your Vercel URL** (e.g., `https://your-app.vercel.app`)

2. **Open Browser DevTools** (F12):
   - Go to **Console** tab
   - Look for: `API Base URL: https://your-railway-url.railway.app/api`
   - Should NOT show the placeholder `https://your-api.railway.app/api`

3. **Check the app:**
   - Should show: **🟢 API Connected** (green)
   - Try generating a schedule
   - Should work without "Failed to fetch" errors

---

### Step 5B: Alternative - Update Code Directly

If setting environment variables doesn't work, update the code:

1. **Edit `frontend/src/api.ts`:**
   - Find line 10
   - Replace: `'https://your-api.railway.app/api'`
   - With: `'https://your-actual-railway-url.railway.app/api'`

2. **Commit and push:**
   ```bash
   git add frontend/src/api.ts
   git commit -m "Update API URL to Railway backend"
   git push
   ```

3. **Vercel will automatically redeploy**

---

## 🔧 Quick Diagnostic Commands

### For Local:
```bash
# Check if backend is running
curl http://localhost:5001/api/health

# Check what's using port 5001
lsof -ti:5001

# Start backend
python api.py
```

### For Production:
```bash
# Test Railway backend
curl https://your-railway-url.railway.app/api/health

# Check Railway logs (in Railway dashboard)
# Settings → View Logs
```

---

## ✅ Success Checklist

### Local Development:
- [ ] Backend is running (`python api.py`)
- [ ] Backend responds to `http://localhost:5001/api/health`
- [ ] Frontend is running (`npm start` in frontend folder)
- [ ] Browser console shows: `API Base URL: http://localhost:5001/api`
- [ ] App shows: **🟢 API Connected**

### Production (Vercel):
- [ ] Railway backend is deployed and running
- [ ] Railway backend responds to health check
- [ ] `REACT_APP_API_URL` is set in Vercel environment variables
- [ ] Value includes `/api` at the end
- [ ] Frontend has been redeployed after setting environment variable
- [ ] Browser console shows correct Railway URL (not placeholder)
- [ ] App shows: **🟢 API Connected**

---

## 🆘 Still Not Working?

1. **Check the exact error message:**
   - Open browser console (F12)
   - Copy the full error message
   - Check the Network tab for failed requests

2. **Verify backend is accessible:**
   - Test the health endpoint directly
   - Check backend logs for errors

3. **Check CORS:**
   - Look for CORS errors in browser console
   - Verify `flask-cors` is installed and configured

4. **Check environment variables:**
   - For Vercel: Verify `REACT_APP_API_URL` is set correctly
   - For Railway: Verify `GEMINI_API_KEY` is set

---

## 📞 Need More Help?

Share these details:
1. Are you running locally or on Vercel?
2. What does `curl http://localhost:5001/api/health` return? (for local)
3. What does the browser console show? (F12 → Console)
4. What's the exact error message?
