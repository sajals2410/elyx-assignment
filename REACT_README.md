# React Frontend - Resource Allocator

## 🚀 Quick Start

### 1. Start the Flask API Backend

```bash
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate
python api.py
```

The API will run on `http://localhost:5000`

### 2. Start the React Frontend

In a new terminal:

```bash
cd /Users/sajalsingh/Desktop/projectelyx/frontend
npm start
```

The React app will open at `http://localhost:3000`

## 📁 Project Structure

```
projectelyx/
├── api.py                 # Flask API backend
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── ConfigPanel.tsx
│   │   │   ├── StatisticsDashboard.tsx
│   │   │   ├── ScheduleViewer.tsx
│   │   │   └── DownloadPanel.tsx
│   │   ├── api.ts        # API service
│   │   ├── App.tsx       # Main app component
│   │   └── index.tsx
│   └── package.json
└── requirements.txt
```

## 🎨 Features

### React Frontend Components

1. **ConfigPanel** - Schedule configuration (date, weeks, data options)
2. **StatisticsDashboard** - Visual statistics with charts
3. **ScheduleViewer** - Interactive schedule by date
4. **DownloadPanel** - Download outputs in various formats

### API Endpoints

- `GET /api/health` - Health check
- `POST /api/generate-data` - Generate test data
- `POST /api/generate-schedule` - Generate schedule
- `GET /api/schedule` - Get current schedule
- `GET /api/statistics` - Get statistics
- `GET /api/download/<type>` - Download files

## 🔧 Development

### Install Dependencies

**Backend:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

### Run Development Servers

**Terminal 1 - Backend:**
```bash
source venv/bin/activate
python api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

### Build for Production

```bash
cd frontend
npm run build
```

The built files will be in `frontend/build/`

## 🎯 Usage

1. **Start both servers** (API and React)
2. **Open browser** to `http://localhost:3000`
3. **Configure settings** in the Config Panel
4. **Click "Generate Schedule"**
5. **View statistics** and schedule
6. **Download outputs** as needed

## 🐛 Troubleshooting

### API Connection Issues

- Make sure Flask API is running on port 5000
- Check browser console for CORS errors
- Verify `REACT_APP_API_URL` in `.env` if using custom URL

### Build Issues

- Clear node_modules: `rm -rf node_modules && npm install`
- Clear cache: `npm start -- --reset-cache`

### Port Conflicts

- Change API port in `api.py`: `app.run(port=5001)`
- Change React port: `PORT=3001 npm start`

## 📦 Dependencies

### Frontend
- React 18
- TypeScript
- Axios (for API calls)
- Recharts (for charts)
- date-fns (for date formatting)

### Backend
- Flask
- Flask-CORS
- All existing scheduler modules

## 🌐 Environment Variables

Create `.env` in `frontend/` directory:

```
REACT_APP_API_URL=http://localhost:5000/api
```

## 📝 Notes

- The React app communicates with Flask API via REST
- All schedule generation happens on the backend
- Frontend displays results and handles downloads
- CORS is enabled for local development
