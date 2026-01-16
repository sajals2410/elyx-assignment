# 🚀 Quick Start - React Frontend

## Prerequisites
- Node.js and npm installed
- Python virtual environment set up
- All Python dependencies installed

## Step 1: Install Frontend Dependencies

```bash
cd /Users/sajalsingh/Desktop/projectelyx/frontend
npm install
```

## Step 2: Start the Servers

### Option A: Use the Startup Script (Recommended)

```bash
cd /Users/sajalsingh/Desktop/projectelyx
./start_react.sh
```

### Option B: Manual Start

**Terminal 1 - Start Flask API:**
```bash
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate
python api.py
```

**Terminal 2 - Start React App:**
```bash
cd /Users/sajalsingh/Desktop/projectelyx/frontend
npm start
```

## Step 3: Open in Browser

- React App: http://localhost:3000
- API Health Check: http://localhost:5000/api/health

## 🎯 Using the App

1. **Check API Status** - Green indicator means connected
2. **Configure Schedule**:
   - Select start date
   - Choose number of weeks (1-24)
   - Optionally regenerate test data
3. **Click "Generate Schedule"**
4. **View Results**:
   - Statistics dashboard with charts
   - Schedule viewer (select dates)
   - Download outputs

## 📱 Features

- ✅ Modern, responsive UI
- ✅ Real-time statistics with charts
- ✅ Interactive schedule viewer
- ✅ Download outputs (Text, HTML, iCal, JSON)
- ✅ API connection status indicator
- ✅ Error handling and loading states

## 🛠️ Troubleshooting

### Port Already in Use

**Change API port:**
Edit `api.py` line: `app.run(port=5001)`

**Change React port:**
```bash
PORT=3001 npm start
```

### API Connection Failed

1. Make sure Flask API is running
2. Check `http://localhost:5000/api/health`
3. Check browser console for errors

### Build Errors

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

## 📦 What's Included

- **Flask API** (`api.py`) - REST API backend
- **React Frontend** (`frontend/`) - Modern UI
- **Components**:
  - ConfigPanel - Schedule configuration
  - StatisticsDashboard - Charts and stats
  - ScheduleViewer - Interactive schedule
  - DownloadPanel - File downloads

## 🎨 UI Highlights

- Gradient backgrounds
- Responsive design (mobile-friendly)
- Color-coded activity types
- Interactive charts (Recharts)
- Smooth animations
- Modern card-based layout

Enjoy your new React frontend! 🎉
