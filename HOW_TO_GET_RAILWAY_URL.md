# Step-by-Step: How to Get Your Railway Backend URL

## 🚂 Step 1: Log in to Railway

1. **Open your web browser**
2. **Go to:** https://railway.app
3. **Click "Log In"** (top right corner)
4. **Sign in** using:
   - GitHub (recommended - if you connected your repo)
   - Email
   - Google
   - Or any other method you used

---

## 📦 Step 2: Find Your Project

After logging in, you'll see your **Railway Dashboard**:

1. **Look for your project** in the list
   - Projects are shown as cards/boxes
   - Your project name should be visible (e.g., "projectelyx" or your repo name)

2. **Click on your project** to open it

**If you don't see your project:**
- Click **"New Project"** (top right)
- Select **"Deploy from GitHub repo"**
- Choose your repository
- Railway will start deploying

---

## 🔍 Step 3: Access Your Service

Once inside your project:

1. **You'll see your services** (usually one service per project)
2. **Click on your service** (it might be named after your repo or "web" or "api")
   - It's usually the main/only service shown

---

## 🌐 Step 4: Get the URL - Method 1 (Settings)

1. **Click on your service** to open it
2. **Look for tabs** at the top:
   - Deployments
   - Metrics
   - Settings
   - Variables
   - Networking
   - etc.

3. **Click on "Settings"** tab

4. **Scroll down** to find **"Networking"** section

5. **Look for "Public Domain"** or **"Custom Domain"**
   - You'll see a URL like: `https://your-project-name.up.railway.app`
   - Or: `https://your-project-name-production.up.railway.app`

6. **Copy this URL** - this is your Railway backend URL!

---

## 🌐 Step 4: Get the URL - Method 2 (Service Overview)

1. **Click on your service** to open it
2. **Look at the top of the page** - you might see:
   - A **"Public URL"** or **"Domain"** section
   - A clickable link showing your URL
   - Example: `https://projectelyx-production.up.railway.app`

3. **Click the copy icon** (📋) next to the URL, or manually copy it

---

## 🌐 Step 4: Get the URL - Method 3 (Deployments Tab)

1. **Click on "Deployments"** tab
2. **Find your latest deployment** (should be at the top)
3. **Click on the deployment** to view details
4. **Look for "Public URL"** or **"Domain"** in the deployment details
5. **Copy the URL**

---

## ✅ Step 5: Verify Your URL

Before using the URL, test it:

1. **Open a new browser tab**
2. **Paste your Railway URL** + `/api/health`
   - Example: `https://projectelyx-production.up.railway.app/api/health`
3. **Press Enter**

**Expected result:**
```json
{
  "status": "ok",
  "message": "Resource Allocator API is running"
}
```

**If you see this:** ✅ Your backend is working!

**If you get an error:**
- Check that your Railway deployment completed successfully
- Check Railway logs for errors
- Make sure `GEMINI_API_KEY` is set in Railway environment variables

---

## 📝 Step 6: Format for Vercel

Your Railway URL should look like:
```
https://projectelyx-production.up.railway.app
```

**For Vercel environment variable, add `/api` at the end:**
```
https://projectelyx-production.up.railway.app/api
```

**Important:** 
- Include `https://` at the beginning
- Include `/api` at the end
- No trailing slash after `/api`

---

## 🖼️ Visual Guide

### Railway Dashboard Layout:
```
┌─────────────────────────────────────┐
│  Railway Dashboard                  │
│                                     │
│  ┌─────────────┐  ┌─────────────┐  │
│  │  Project 1  │  │  Project 2  │  │
│  │  (Click)    │  │             │  │
│  └─────────────┘  └─────────────┘  │
└─────────────────────────────────────┘
```

### Inside Project:
```
┌─────────────────────────────────────┐
│  Your Project Name                  │
│                                     │
│  [Deployments] [Settings] [Variables]│
│                                     │
│  Service: web                       │
│  ┌───────────────────────────────┐  │
│  │ Public URL:                  │  │
│  │ https://xxx.up.railway.app   │  │
│  │ [📋 Copy]                    │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 🆘 Troubleshooting

### Can't find the URL?

1. **Check if deployment completed:**
   - Go to "Deployments" tab
   - Look for a green checkmark ✅
   - If it's still deploying, wait for it to finish

2. **Check if service is running:**
   - Go to "Metrics" tab
   - Should show CPU/Memory usage
   - If all zeros, service might not be running

3. **Check environment variables:**
   - Go to "Variables" tab
   - Make sure `GEMINI_API_KEY` is set
   - Railway might not start without required variables

### URL shows "Not Found" or 404?

- Make sure your backend code is deployed
- Check Railway logs for errors
- Verify `api.py` is the entry point (check `Procfile` or `railway.json`)

### Can't access Railway dashboard?

- Make sure you're logged in
- Check if you have access to the project
- Try logging out and back in

---

## 📋 Quick Checklist

- [ ] Logged into Railway
- [ ] Found your project
- [ ] Clicked on your service
- [ ] Found the Public URL/Domain
- [ ] Copied the URL (e.g., `https://xxx.up.railway.app`)
- [ ] Tested URL + `/api/health` - got OK response
- [ ] Ready to use in Vercel as: `https://xxx.up.railway.app/api`

---

## 🎯 Next Steps

Once you have your Railway URL:

1. **Copy it** (e.g., `https://projectelyx-production.up.railway.app`)
2. **Add `/api`** to the end: `https://projectelyx-production.up.railway.app/api`
3. **Go to Vercel** → Settings → Environment Variables
4. **Add:** `REACT_APP_API_URL` = `https://your-railway-url.railway.app/api`
5. **Redeploy** your Vercel frontend

Your app should now connect to your Railway backend! 🎉
