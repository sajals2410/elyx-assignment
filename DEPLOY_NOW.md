# 🚀 FINAL DEPLOYMENT INSTRUCTIONS

## ✅ Everything is Ready!

All files are prepared. Follow these exact steps:

---

## 📋 STEP-BY-STEP DEPLOYMENT

### Step 1: Commit and Push to GitHub

```bash
cd /Users/sajalsingh/Desktop/projectelyx

# Add all changes
git add .

# Commit
git commit -m "Complete project: Vercel frontend + Railway backend setup"

# Push to GitHub
git push origin main
```

---

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
   - Click **Generate Domain**
   - Copy the URL (e.g., `https://projectelyx-production.up.railway.app`)
   - **Save this URL!**

---

### Step 3: Update Frontend API URL

**Option A: Update Code (Quick)**

Edit `frontend/src/api.ts`:
```typescript
const API_BASE_URL = 'https://YOUR-RAILWAY-URL.railway.app/api';
```
Replace `YOUR-RAILWAY-URL` with your actual Railway URL.

**Option B: Use Environment Variable (Better)**

1. Go to Vercel Dashboard: https://vercel.com/dashboard
2. Select your project: `projectelyx`
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Name: `REACT_APP_API_URL`
6. Value: `https://YOUR-RAILWAY-URL.railway.app/api`
7. Environments: Production, Preview, Development (select all)
8. Click **Save**

---

### Step 4: Deploy Frontend to Vercel

```bash
cd /Users/sajalsingh/Desktop/projectelyx
npx vercel --prod
```

---

### Step 5: Test Everything

1. **Test Railway Backend:**
   ```bash
   curl https://YOUR-RAILWAY-URL.railway.app/api/health
   ```
   Should return: `{"status":"ok","message":"Resource Allocator API is running"}`

2. **Test Frontend:**
   - Open your Vercel URL: `https://projectelyx.vercel.app`
   - Check API status (should be green)
   - Generate a schedule
   - Verify it works!

---

## 🎯 Final Architecture

```
┌─────────────────────┐
│  React Frontend     │
│  (Vercel)           │
│  projectelyx.vercel │
│  .app               │
└──────────┬──────────┘
           │
           │ API Calls
           │
           ▼
┌─────────────────────┐
│  Flask API          │
│  (Railway)          │
│  your-api.railway   │
│  .app               │
└─────────────────────┘
```

---

## ✅ Checklist

- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Backend deployed to Railway
- [ ] GEMINI_API_KEY set in Railway
- [ ] Railway URL copied
- [ ] Frontend API URL updated
- [ ] Frontend deployed to Vercel
- [ ] Tested backend API
- [ ] Tested frontend app

---

## 🆘 If Something Goes Wrong

**Railway Issues:**
- Check Railway logs: Dashboard → Service → Logs
- Verify `requirements.txt` is correct
- Check that `api.py` exists in root

**Vercel Issues:**
- Check Vercel logs: Dashboard → Project → Logs
- Verify environment variables are set
- Check that frontend builds successfully

**CORS Issues:**
- Already handled in `api.py` with `CORS(app)`
- Should work automatically

---

## 🎉 You're Done!

After completing these steps:
- ✅ Backend running on Railway
- ✅ Frontend running on Vercel
- ✅ Full-stack app deployed and working!

**Your app will be live at:** `https://projectelyx.vercel.app`

---

**Need help?** Check the logs in Railway and Vercel dashboards for specific errors.
