# 🚀 Vercel Deployment Guide

Complete guide to deploy Resource Allocator on Vercel with React frontend and Python backend.

## 📋 Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install globally
   ```bash
   npm install -g vercel
   ```
3. **Git Repository**: Your project should be in a Git repository (GitHub, GitLab, or Bitbucket)

## 🏗️ Project Structure

```
projectelyx/
├── api/                    # Vercel serverless functions
│   ├── health.py
│   ├── generate-data.py
│   ├── generate-schedule.py
│   ├── schedule.py
│   ├── statistics.py
│   ├── download.py
│   └── activities.py
├── frontend/               # React frontend
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vercel.json
├── vercel.json             # Root Vercel configuration
├── requirements.txt        # Python dependencies
└── ... (other files)
```

## 🔧 Setup Steps

### 1. Install Dependencies

**Frontend:**
```bash
cd frontend
npm install
```

**Backend (Python):**
```bash
# Dependencies are automatically installed by Vercel
# But you can test locally with:
pip install -r requirements.txt
```

### 2. Environment Variables

Set these in Vercel Dashboard → Project Settings → Environment Variables:

- `GEMINI_API_KEY` (optional): Your Google Gemini API key for AI-powered data generation

**To set environment variables:**

1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: Your API key
   - **Environment**: Production, Preview, Development (select all)

### 3. Deploy to Vercel

#### Option A: Using Vercel CLI (Recommended)

```bash
# Login to Vercel
vercel login

# Deploy (from project root)
vercel

# For production deployment
vercel --prod
```

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your Git repository
3. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`
4. Add environment variables (see step 2)
5. Click "Deploy"

### 4. Configure Vercel Settings

In your Vercel project settings, ensure:

**Build & Development Settings:**
- **Framework Preset**: Create React App
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

**Functions:**
- **Python Version**: 3.11
- **Max Duration**: 60 seconds (for schedule generation)

## 📁 File Structure for Vercel

### Root `vercel.json`

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
    },
    {
      "src": "api/**/*.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "/api/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/frontend/$1"
    }
  ]
}
```

### API Serverless Functions

All API endpoints are in `/api/` directory:
- `health.py` - Health check
- `generate-data.py` - Generate test data
- `generate-schedule.py` - Generate schedule
- `schedule.py` - Get schedule
- `statistics.py` - Get statistics
- `download.py` - Download files
- `activities.py` - Get activities

## 🔄 API Endpoints

After deployment, your API will be available at:
- Production: `https://your-project.vercel.app/api/`
- Preview: `https://your-project-git-branch.vercel.app/api/`

**Available endpoints:**
- `GET /api/health` - Health check
- `POST /api/generate-data` - Generate data
- `POST /api/generate-schedule` - Generate schedule
- `GET /api/schedule` - Get schedule
- `GET /api/statistics` - Get statistics
- `GET /api/download/<type>` - Download files
- `GET /api/activities` - Get activities

## 🧪 Testing Locally

### Test with Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Run development server
vercel dev
```

This will:
- Start React frontend on `http://localhost:3000`
- Start API serverless functions on `http://localhost:3000/api/`

### Test API Endpoints

```bash
# Health check
curl http://localhost:3000/api/health

# Generate data
curl -X POST http://localhost:3000/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "duration_months": 3}'
```

## 🐛 Troubleshooting

### Issue: API endpoints return 404

**Solution:**
- Ensure `api/` directory is in the root (not inside `frontend/`)
- Check `vercel.json` routes configuration
- Verify function files have `.py` extension

### Issue: Module not found errors

**Solution:**
- Ensure all Python dependencies are in `requirements.txt`
- Check that modules are imported correctly in API functions
- Verify Python version is 3.11 in Vercel settings

### Issue: CORS errors

**Solution:**
- CORS is handled in each API function
- Ensure `Access-Control-Allow-Origin: *` is in response headers
- Check that API calls use relative URLs in production

### Issue: File downloads not working

**Solution:**
- Download endpoint returns base64 encoded data
- Frontend decodes and creates blob for download
- Check browser console for errors

### Issue: Timeout errors

**Solution:**
- Schedule generation can take time
- Increase function timeout in Vercel settings (max 60s for Hobby plan)
- Consider optimizing the scheduling algorithm for large datasets

## 📊 Monitoring

### View Logs

```bash
# View deployment logs
vercel logs

# View function logs in dashboard
# Vercel Dashboard → Your Project → Functions → View Logs
```

### Check Function Performance

1. Go to Vercel Dashboard
2. Navigate to Functions tab
3. View execution time and errors

## 🔐 Security Considerations

1. **API Keys**: Store in Vercel environment variables (never commit)
2. **CORS**: Configured for all origins (adjust for production if needed)
3. **Rate Limiting**: Consider adding rate limiting for production
4. **Input Validation**: Validate all API inputs

## 🚀 Production Checklist

- [ ] Environment variables set in Vercel
- [ ] All API endpoints tested
- [ ] Frontend builds successfully
- [ ] CORS configured correctly
- [ ] Error handling in place
- [ ] Logging configured
- [ ] Performance optimized
- [ ] Security measures in place

## 📝 Notes

### File Storage

Vercel serverless functions are stateless. Files are stored in `/tmp` directory:
- Data files: `/tmp/data/`
- Output files: `/tmp/output/`

**Important**: Files in `/tmp` are ephemeral and cleared between function invocations. For persistent storage, consider:
- Vercel Blob Storage
- External database (PostgreSQL, MongoDB)
- Cloud storage (AWS S3, Google Cloud Storage)

### Current Limitations

1. **File Persistence**: Generated files are not persisted between requests
2. **Function Timeout**: Maximum 60 seconds (Hobby plan)
3. **Memory**: Limited memory per function execution

### Future Improvements

1. Add database for persistent storage
2. Implement caching for generated schedules
3. Add rate limiting
4. Implement authentication if needed
5. Add monitoring and analytics

## 🆘 Support

If you encounter issues:

1. Check Vercel deployment logs
2. Review function logs in dashboard
3. Test endpoints individually
4. Verify environment variables
5. Check Vercel documentation: [vercel.com/docs](https://vercel.com/docs)

---

**Ready to deploy!** Follow the steps above to get your Resource Allocator running on Vercel! 🎉
