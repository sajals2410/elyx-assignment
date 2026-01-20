# 🚀 DEPLOY TO RAILWAY NOW - Step by Step

## ⚠️ Current Issue
Vercel Python functions are timing out. This is a known limitation.

## ✅ Solution: Deploy Backend to Railway

---

## STEP 1: Prepare Code (Do This First)

```bash
cd /Users/sajalsingh/Desktop/projectelyx

# Make sure everything is committed
git add .
git commit -m "Ready for Railway deployment"
git push origin main
```

---

## STEP 2: Deploy to Railway (5 minutes)

### 2.1 Go to Railway
1. Open: https://railway.app
2. Click **"Start a New Project"** or **"Login"**
3. Sign up with GitHub (easiest way)

### 2.2 Create Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Authorize Railway (if first time)
4. Select your repository: `elyx-assignment` (or your repo name)

### 2.3 Configure
1. Railway will **auto-detect** Python/Flask
2. It will automatically:
   - Find `requirements.txt`
   - Find `api.py`
   - Start the Flask server

### 2.4 Add Environment Variable
1. Click on your service (the one that was created)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add:
   - **Name**: `GEMINI_API_KEY`
   - **Value**: `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
5. Click **"Add"**

### 2.5 Get Your URL
1. Go to **"Settings"** tab
2. Scroll to **"Domains"** section
3. Click **"Generate Domain"** (or use existing)
4. **Copy the URL** (e.g., `https://projectelyx-production.up.railway.app`)
5. **SAVE THIS URL!**

---

## STEP 3: Update Frontend

### 3.1 Edit API URL
Open: `frontend/src/api.ts`

Find line 10:
```typescript
? 'https://your-api.railway.app/api'  // Update with your Railway URL
```

Replace with your Railway URL:
```typescript
? 'https://projectelyx-production.up.railway.app/api'  // Your actual Railway URL
```

### 3.2 Commit and Push
```bash
git add frontend/src/api.ts
git commit -m "Update API URL to Railway backend"
git push origin main
```

---

## STEP 4: Redeploy Frontend to Vercel

```bash
npx vercel --prod
```

Or:
1. Go to Vercel Dashboard
2. Your project → **Deployments**
3. Click **"Redeploy"** on latest deployment

---

## STEP 5: Test

1. **Test Railway Backend:**
   ```bash
   curl https://your-api.railway.app/api/health
   ```
   Should return: `{"status":"ok","message":"Resource Allocator API is running"}`

2. **Test Frontend:**
   - Open: `https://projectelyx.vercel.app`
   - Should work now! ✅

---

## 🎯 What This Does

```
Before (Not Working):
Frontend (Vercel) → Python Functions (Vercel) ❌ TIMEOUT

After (Working):
Frontend (Vercel) → Flask API (Railway) ✅ WORKS!
```

---

## ⏱️ Time Required
- Railway setup: 5 minutes
- Frontend update: 2 minutes
- Total: ~7 minutes

---

## 🆘 Need Help?

**Railway Issues:**
- Check logs: Railway Dashboard → Service → Logs
- Verify `GEMINI_API_KEY` is set
- Check that deployment succeeded

**Still Timeout?**
- Make sure you updated `frontend/src/api.ts` with Railway URL
- Hard refresh browser: Cmd+Shift+R
- Check browser console (F12) for errors

---

**This will fix the timeout completely!** 🚀
