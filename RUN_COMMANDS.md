# 🚀 Commands to Run the Project

## 📋 Quick Reference

### Local Development (Before Vercel)

#### 1. Setup (First Time Only)

```bash
# Navigate to project directory
cd /Users/sajalsingh/Desktop/projectelyx

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..
```

#### 2. Run Locally (Development Mode)

**Option A: Run Flask API + React (Traditional)**

```bash
# Terminal 1: Start Flask API
source venv/bin/activate
python api.py
# API runs on http://localhost:5001

# Terminal 2: Start React Frontend
cd frontend
npm start
# Frontend runs on http://localhost:3000
```

**Option B: Run with Streamlit (Alternative)**

```bash
source venv/bin/activate
streamlit run app.py
# Runs on http://localhost:8501
```

**Option C: Run CLI Tool**

```bash
source venv/bin/activate
python main.py --weeks 2
```

---

## 🌐 Vercel Deployment Commands

### 1. Install Vercel CLI (Local - No Global Install Needed)

```bash
# From frontend directory (already installed)
cd frontend
# Vercel is already installed locally
npx vercel --version
```

### 2. Login to Vercel

```bash
# From project root
cd /Users/sajalsingh/Desktop/projectelyx
cd frontend
npx vercel login
```

### 3. Deploy to Vercel

```bash
# From project root
cd /Users/sajalsingh/Desktop/projectelyx

# Deploy (preview)
npx vercel

# Deploy to production
npx vercel --prod
```

### 4. Test Deployment Locally (Vercel Dev)

```bash
# From project root
cd /Users/sajalsingh/Desktop/projectelyx

# Install Vercel CLI locally if not already
cd frontend
npm install vercel --save-dev

# Run Vercel dev server (simulates production)
cd ..
npx vercel dev
# Runs on http://localhost:3000
```

---

## 🧪 Testing Commands

### Test API Endpoints Locally

```bash
# Health check
curl http://localhost:5001/api/health

# Generate data
curl -X POST http://localhost:5001/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "duration_months": 3}'

# Generate schedule
curl -X POST http://localhost:5001/api/generate-schedule \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "weeks": 2}'
```

### Test Vercel Functions Locally

```bash
# After running: npx vercel dev

# Health check
curl http://localhost:3000/api/health

# Generate data
curl -X POST http://localhost:3000/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "duration_months": 3}'
```

---

## 🔧 Utility Commands

### Check Project Status

```bash
# Check Python version
python --version

# Check Node version
node --version

# Check installed packages
pip list
npm list --depth=0

# Check Git status
git status
```

### Clean Up

```bash
# Remove Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# Remove node_modules (if needed)
rm -rf frontend/node_modules
rm -rf frontend/build

# Remove generated files
rm -rf data/*.json data/*.csv
rm -rf output/*
```

### Reinstall Dependencies

```bash
# Python
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

## 📊 Environment Variables

### Set Environment Variables Locally

```bash
# For local development
export GEMINI_API_KEY='your_api_key_here'

# Or create .env file (already in .gitignore)
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

### Set Environment Variables in Vercel

```bash
# Via CLI
npx vercel env add GEMINI_API_KEY

# Or via Dashboard:
# 1. Go to vercel.com
# 2. Select your project
# 3. Settings → Environment Variables
# 4. Add GEMINI_API_KEY
```

---

## 🎯 Common Workflows

### Workflow 1: Quick Local Test

```bash
# Terminal 1
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate
python api.py

# Terminal 2
cd /Users/sajalsingh/Desktop/projectelyx/frontend
npm start

# Open browser: http://localhost:3000
```

### Workflow 2: Deploy to Vercel

```bash
cd /Users/sajalsingh/Desktop/projectelyx

# Login (first time)
cd frontend
npx vercel login

# Deploy
cd ..
npx vercel --prod
```

### Workflow 3: Test Vercel Locally

```bash
cd /Users/sajalsingh/Desktop/projectelyx
npx vercel dev

# Open browser: http://localhost:3000
```

---

## 🐛 Troubleshooting Commands

### Check if Ports are in Use

```bash
# Check port 5001 (Flask)
lsof -ti:5001

# Check port 3000 (React)
lsof -ti:3000

# Kill process on port
kill -9 $(lsof -ti:5001)
```

### Check Logs

```bash
# Vercel logs
npx vercel logs

# Python errors
python api.py 2>&1 | tee api.log

# React errors
cd frontend
npm start 2>&1 | tee ../react.log
```

### Verify Installation

```bash
# Check Python packages
pip show flask flask-cors

# Check Node packages
cd frontend
npm list react react-dom
```

---

## 📝 Quick Command Cheat Sheet

```bash
# ============================================
# SETUP (First Time)
# ============================================
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend && npm install && cd ..

# ============================================
# LOCAL DEVELOPMENT
# ============================================
# Terminal 1: API
source venv/bin/activate && python api.py

# Terminal 2: Frontend
cd frontend && npm start

# ============================================
# VERCEL DEPLOYMENT
# ============================================
# Login
cd frontend && npx vercel login

# Deploy
cd .. && npx vercel --prod

# Test locally
npx vercel dev

# ============================================
# TESTING
# ============================================
# API Health
curl http://localhost:5001/api/health

# Generate Schedule
curl -X POST http://localhost:5001/api/generate-schedule \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "weeks": 2}'
```

---

## 🎯 Recommended: Start Here

**For Local Development:**
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Start API (Terminal 1)
python api.py

# 3. Start Frontend (Terminal 2)
cd frontend
npm start
```

**For Vercel Deployment:**
```bash
# 1. Login (first time)
cd frontend
npx vercel login

# 2. Deploy
cd ..
npx vercel --prod
```

---

**Need help?** Check `VERCEL_DEPLOYMENT.md` for detailed deployment guide!
