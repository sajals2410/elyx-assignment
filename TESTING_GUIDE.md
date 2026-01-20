# 🧪 Testing Guide - Resource Allocator

## Quick Test Options

### Option 1: Test Without Gemini API Key (Templates)

This tests the fallback mechanism - works immediately:

```bash
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate

# Test 1: Quick schedule generation
python main.py --weeks 1 --no-preview

# Test 2: Check outputs
ls -lh output/
cat output/schedule_summary.json | python -m json.tool | head -30
```

**Expected Result:**
- ✅ Schedule generated successfully
- ✅ Output files created
- ✅ Uses template-based generation

---

### Option 2: Test Gemini Integration (With API Key)

**Step 1: Get API Key**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy your key

**Step 2: Set API Key**
```bash
export GEMINI_API_KEY='your_api_key_here'
```

**Step 3: Test Gemini Connection**
```bash
python test_gemini.py
```

**Expected Result:**
- ✅ API key found
- ✅ Generator created
- ✅ Gemini API is working

**Step 4: Generate Data with Gemini**
```bash
python -c "
from data_generator_gemini import GeminiDataGenerator
generator = GeminiDataGenerator('2026-01-15', 1)
data = generator.save_all_data('data')
print(f'Generated {len(data[\"activities\"])} activities')
"
```

**Step 5: Full Test with Gemini**
```bash
python main.py --weeks 2
```

**Expected Result:**
- ✅ "🤖 Generating activities with Gemini AI..."
- ✅ "✅ Generated X activities with Gemini AI"
- ✅ Schedule generated successfully

---

### Option 3: Test via Web Interface

**Step 1: Start API Server**
```bash
# Terminal 1
source venv/bin/activate
python api.py
```

**Step 2: Start React App**
```bash
# Terminal 2
cd frontend
npm start
```

**Step 3: Test in Browser**
1. Open http://localhost:3000
2. Check "🤖 Use Gemini AI" checkbox (if API key set)
3. Check "Regenerate Test Data"
4. Click "🚀 Generate Schedule"
5. Watch for:
   - Loading indicator
   - Success message
   - Statistics displayed
   - Schedule viewer working

---

## Detailed Test Scenarios

### Test 1: Verify Fallback Works

```bash
# Don't set API key
unset GEMINI_API_KEY
python main.py --weeks 1 --no-preview
```

**Check:**
- ✅ No errors
- ✅ Schedule generated
- ✅ Uses templates

### Test 2: Verify Gemini Works

```bash
# Set API key
export GEMINI_API_KEY='your_key'
python main.py --weeks 1 --no-preview
```

**Check:**
- ✅ "🤖 Generating activities with Gemini AI..."
- ✅ Activities generated
- ✅ Schedule created

### Test 3: Test API Endpoint

```bash
# Start API
python api.py

# In another terminal, test endpoint
curl -X POST http://localhost:5001/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "duration_months": 1, "use_gemini": true}'
```

**Check Response:**
```json
{
  "success": true,
  "method": "Gemini AI" or "Template-based",
  "activities": 105
}
```

### Test 4: Test React Frontend

```bash
# Start both servers
python api.py  # Terminal 1
cd frontend && npm start  # Terminal 2
```

**Test Steps:**
1. Open http://localhost:3000
2. Verify API status shows "🟢 API Connected"
3. Configure settings
4. Generate schedule
5. Check statistics display
6. View schedule by date
7. Download files

---

## Verification Checklist

### ✅ Basic Functionality
- [ ] Schedule generates without errors
- [ ] Output files created (HTML, iCal, JSON, Text)
- [ ] Statistics are accurate
- [ ] Activities are scheduled correctly

### ✅ Gemini Integration
- [ ] Falls back gracefully without API key
- [ ] Uses Gemini when API key is set
- [ ] Generates diverse activities with AI
- [ ] No errors if API fails

### ✅ API Endpoints
- [ ] Health check works
- [ ] Data generation works
- [ ] Schedule generation works
- [ ] Statistics endpoint works
- [ ] Download endpoints work

### ✅ Frontend
- [ ] Page loads correctly
- [ ] API connection status shows
- [ ] Configuration panel works
- [ ] Statistics display correctly
- [ ] Schedule viewer works
- [ ] Downloads work
- [ ] Gemini toggle works

---

## Quick Test Commands

### One-Line Tests

```bash
# Test 1: Quick generation
python main.py --weeks 1 --no-preview && echo "✅ Success"

# Test 2: Check outputs
ls output/*.html output/*.ics output/*.json && echo "✅ Files created"

# Test 3: Test API health
curl http://localhost:5001/api/health && echo "✅ API working"

# Test 4: Test Gemini (if key set)
python test_gemini.py

# Test 5: Verify data structure
python -c "from scheduler import load_data; a,_,_,_,_,_ = load_data('data'); print(f'✅ {len(a)} activities loaded')"
```

---

## Troubleshooting Tests

### If Gemini Test Fails

```bash
# Check API key
echo $GEMINI_API_KEY

# Test connection
python -c "import google.generativeai as genai; genai.configure(api_key='$GEMINI_API_KEY'); print('✅ API key valid')"

# Check internet
curl -I https://generativelanguage.googleapis.com
```

### If API Fails

```bash
# Check if API is running
lsof -ti:5001

# Check API logs
tail -f api.log  # if using nohup

# Test health endpoint
curl http://localhost:5001/api/health
```

### If React Fails

```bash
# Check if React is running
lsof -ti:3000

# Check for errors
cd frontend
npm run build  # Check for build errors

# Clear cache
rm -rf node_modules/.cache
npm start
```

---

## Expected Test Results

### Without API Key
```
⚠️  GEMINI_API_KEY not set. Using template-based generation.
📊 GENERATING TEST DATA
Generating activities...
✅ Generated 105 activities
✅ Schedule generated successfully!
```

### With API Key
```
🤖 Generating activities with Gemini AI...
   Generating 20 fitness activities...
   Generating 15 food activities...
✅ Generated 105 activities with Gemini AI
✅ Schedule generated successfully!
```

---

## Performance Tests

```bash
# Test generation speed
time python main.py --weeks 2 --no-preview

# Test with different week counts
for weeks in 1 2 4 8; do
  echo "Testing $weeks weeks..."
  time python main.py --weeks $weeks --no-preview
done
```

---

## Integration Tests

### Full Workflow Test

```bash
# 1. Generate data
python main.py --generate-only

# 2. Generate schedule
python main.py --schedule-only --weeks 2

# 3. Check outputs
ls -lh output/

# 4. Verify schedule
python -c "
from scheduler import load_data
from calendar_output import CalendarFormatter
activities, _, _, _, _, _ = load_data('data')
formatter = CalendarFormatter([])
print('✅ All modules work together')
"
```

---

**Ready to test!** Follow the steps above to verify everything works! 🚀
