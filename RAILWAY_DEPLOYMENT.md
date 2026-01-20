# 🚂 Railway Deployment Guide - Flask Backend

## Quick Deploy Steps

### Step 1: Push Code to GitHub

```bash
git add .
git commit -m "Prepare for Railway deployment"
git push origin main
```

### Step 2: Deploy to Railway

1. **Go to Railway**: https://railway.app
2. **Sign up/Login** (use GitHub)
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**: `elyx-assignment` (or your repo name)
5. **Railway will auto-detect** Python/Flask
6. **Click Deploy**

### Step 3: Configure Environment Variables

1. In Railway dashboard → Your service
2. **Variables** tab
3. **Add Variable**:
   - Name: `GEMINI_API_KEY`
   - Value: `AIzaSyBmdA0E4asvowq0K7WDqbDCJg7Un7bW3VA`
4. **Save**

### Step 4: Get Your API URL

1. Railway dashboard → Your service
2. **Settings** → **Generate Domain**
3. Copy the URL (e.g., `https://your-api.railway.app`)

### Step 5: Update Frontend

**Option A: Environment Variable (Recommended)**

1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add:
   - Name: `REACT_APP_API_URL`
   - Value: `https://your-api.railway.app/api`
3. Redeploy frontend: `npx vercel --prod`

**Option B: Update Code Directly**

Edit `frontend/src/api.ts`:
```typescript
const API_BASE_URL = 'https://your-api.railway.app/api';
```

Then redeploy: `npx vercel --prod`

---

## Railway Configuration

Railway uses:
- `Procfile` - Start command
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version (optional)
- Auto-detects Flask/Python

---

## Testing

After deployment, test:

```bash
# Health check
curl https://your-api.railway.app/api/health

# Should return:
# {"status":"ok","message":"Resource Allocator API is running"}
```

---

## Troubleshooting

**If Railway doesn't detect Python:**
- Make sure `requirements.txt` exists
- Check that `api.py` is in root directory
- Verify `Procfile` exists

**If API doesn't start:**
- Check Railway logs
- Verify PORT environment variable is set
- Check that `api.py` runs locally

**If CORS errors:**
- Already configured in `api.py` with `CORS(app)`
- Should work automatically

---

## Cost

Railway Free Tier:
- $5 credit/month
- More than enough for this project
- Auto-sleeps after inactivity (wakes on request)

---

**Ready to deploy!** Follow the steps above. 🚀
