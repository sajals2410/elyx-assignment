# 🚨 QUICK FIX GUIDE

## If you see "Cannot connect to API" error:

### Step 1: Verify Services Are Running
```bash
# Check API
curl http://localhost:5001/api/health

# Should return: {"status":"ok","message":"Resource Allocator API is running"}
```

### Step 2: Hard Refresh Browser
- **Mac**: `Cmd + Shift + R`
- **Windows/Linux**: `Ctrl + Shift + R`

### Step 3: Clear Browser Cache
1. Open DevTools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"

### Step 4: Check Browser Console
1. Open DevTools (F12)
2. Go to **Console** tab
3. Look for:
   - ✅ "Health check: Connecting to http://localhost:5001/api/health"
   - ✅ "Health check response status: 200"
   - ❌ Any red error messages

### Step 5: Check Network Tab
1. DevTools → **Network** tab
2. Look for `/api/health` request
3. Check:
   - Status: Should be **200**
   - Response Headers: Should include `Access-Control-Allow-Origin`

### Step 6: If Still Not Working

**Restart Everything:**
```bash
./stop_all.sh
./start_api.sh
# Wait 3 seconds
cd frontend && npm start
```

**Or use the fix script:**
```bash
./fix_connection.sh
```

---

## Common Issues:

1. **CORS Error**: Already fixed - API now allows localhost:3000
2. **Port Conflict**: Check if port 5001 is free: `lsof -ti:5001`
3. **API Not Running**: Start with `./start_api.sh`
4. **Frontend Not Running**: Start with `cd frontend && npm start`
5. **Browser Cache**: Hard refresh or clear cache

---

## Diagnostic Command:
```bash
./diagnose.sh
```

This will check everything and tell you what's wrong.

