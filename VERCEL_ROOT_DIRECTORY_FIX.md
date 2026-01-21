# Fix: Vercel "cd frontend: No such file or directory" Error

## 🔍 Problem

The error occurs because Vercel is trying to run `cd frontend` but the `frontend` directory might not be accessible in the build context, or Vercel needs to be configured to use `frontend/` as the root directory.

## ✅ Solution: Set Root Directory in Vercel Dashboard

The **best and recommended solution** is to configure Vercel to use `frontend` as the root directory:

### Step 1: Go to Vercel Dashboard

1. Visit: https://vercel.com
2. Log in and select your project

### Step 2: Go to Settings

1. Click **"Settings"** (top menu)
2. Click **"General"** (left sidebar)

### Step 3: Set Root Directory

1. Scroll down to **"Root Directory"** section
2. Click **"Edit"**
3. Enter: `frontend`
4. Click **"Save"**

### Step 4: Update vercel.json

After setting the root directory, simplify `vercel.json` to:

```json
{
  "version": 2,
  "buildCommand": "npm install && npm run build",
  "outputDirectory": "build"
}
```

Or you can remove `vercel.json` entirely if you've set the root directory in the dashboard, as Vercel will automatically detect `package.json` in the `frontend/` directory.

### Step 5: Redeploy

1. Go to **"Deployments"** tab
2. Click **"..."** on latest deployment
3. Select **"Redeploy"**

---

## 🔧 Alternative: Update vercel.json Only

If you prefer not to use the dashboard, update `vercel.json` to handle the subdirectory:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "build"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ]
}
```

But the **dashboard method is recommended** as it's cleaner and more reliable.

---

## 📋 Summary

**Root Cause:** Vercel doesn't know that `frontend/` is your project root, so it can't find the directory when running `cd frontend`.

**Best Fix:** Set Root Directory to `frontend` in Vercel Dashboard → Settings → General

**Quick Fix:** Update `vercel.json` to use the `builds` configuration with `frontend/package.json`

---

After applying the fix, Vercel will:
1. Treat `frontend/` as the project root
2. Find `package.json` automatically
3. Run `npm install` from the `frontend/` directory
4. Run `npm run build` successfully
5. Output to `frontend/build/`
