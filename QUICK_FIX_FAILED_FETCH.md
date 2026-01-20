# Quick Fix: "Failed to fetch" Error

## 🚀 Immediate Solutions

### If Running Locally:

1. **Start the backend:**
   ```bash
   python api.py
   ```
   Should see: `Running on http://0.0.0.0:5001`

2. **Verify backend is running:**
   - Open: http://localhost:5001/api/health
   - Should see: `{"status": "ok", ...}`

3. **Start the frontend:**
   ```bash
   cd frontend
   npm start
   ```

---

### If Deployed on Vercel:

1. **Get your Railway backend URL:**
   - Go to Railway Dashboard
   - Copy your service URL (e.g., `https://projectelyx-production.up.railway.app`)

2. **Set environment variable in Vercel:**
   - Vercel Dashboard → Settings → Environment Variables
   - Add: `REACT_APP_API_URL` = `https://your-railway-url.railway.app/api`
   - **Important:** Include `/api` at the end!

3. **Redeploy:**
   - Vercel Dashboard → Deployments → Click "..." → Redeploy

---

## 🔍 Check These First:

- [ ] Backend is running (local) or deployed (Railway)
- [ ] API URL is correct (not the placeholder `https://your-api.railway.app/api`)
- [ ] Environment variable `REACT_APP_API_URL` is set in Vercel (if deployed)
- [ ] Railway backend has `GEMINI_API_KEY` environment variable set

---

## 📝 Test Commands:

**Test local backend:**
```bash
curl http://localhost:5001/api/health
```

**Test Railway backend:**
```bash
curl https://your-railway-url.railway.app/api/health
```

Both should return: `{"status": "ok", "message": "Resource Allocator API is running"}`

---

## ⚡ Most Common Issue:

**The API URL is still the placeholder!**

If you see `https://your-api.railway.app/api` in the console, you need to:
1. Set `REACT_APP_API_URL` in Vercel, OR
2. Update `frontend/src/api.ts` line 10 with your actual Railway URL

---

For detailed troubleshooting, see: `TROUBLESHOOTING_FAILED_FETCH.md`
