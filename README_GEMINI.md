# 🤖 Gemini AI Integration - Quick Start

## Overview

The Resource Allocator now uses **Google's Gemini AI** to generate realistic, diverse health activities instead of hardcoded templates. This provides:

- ✨ More diverse and creative activities
- 🎯 Better context understanding
- 📈 Scalable generation
- 🔄 Automatic fallback to templates if API unavailable

## 🚀 Quick Setup

### 1. Get Your Free API Key

Visit: **https://makersuite.google.com/app/apikey**
- Sign in with Google
- Click "Create API Key"
- Copy your key

### 2. Set the API Key

```bash
# Option 1: Environment variable (recommended)
export GEMINI_API_KEY='your_api_key_here'

# Option 2: Add to .env file
echo "GEMINI_API_KEY=your_api_key_here" >> .env
```

### 3. Test It

```bash
# Test Gemini integration
python test_gemini.py

# Or generate data with Gemini
python -c "from data_generator_gemini import GeminiDataGenerator; g = GeminiDataGenerator('2026-01-15', 1); g.save_all_data('data')"
```

## 📖 Usage

### Command Line

```bash
# With Gemini (if API key set)
export GEMINI_API_KEY='your_key'
python main.py --weeks 2

# System automatically uses Gemini if key is available
# Falls back to templates if not
```

### Python Code

```python
from data_generator_gemini import GeminiDataGenerator

# Uses Gemini if API key is set
generator = GeminiDataGenerator(
    start_date="2026-01-15",
    duration_months=3
)
data = generator.save_all_data("data")
```

### React Frontend

The web interface now has a checkbox:
- ✅ "🤖 Use Gemini AI for Activity Generation"
- Automatically uses Gemini if API key is set
- Falls back gracefully if not available

### API Endpoint

```bash
curl -X POST http://localhost:5001/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2026-01-15",
    "duration_months": 3,
    "use_gemini": true
  }'
```

## 🔄 How It Works

1. **Check for API Key**: System checks for `GEMINI_API_KEY`
2. **Generate with AI**: If available, uses Gemini to generate activities
3. **Parse Response**: Converts AI response to Activity objects
4. **Fallback**: If API fails, uses template-based generation
5. **Continue**: Rest of system works normally

## 📊 What Gets Generated

Gemini generates:
- **Activity names**: Creative, realistic names
- **Details**: Specific instructions and parameters
- **Durations**: Appropriate time ranges
- **Facilitators**: Realistic professional names
- **Locations**: Appropriate venues
- **Equipment**: Relevant equipment lists
- **Metrics**: Tracking metrics
- **Frequencies**: Appropriate scheduling frequencies
- **Priorities**: Health-appropriate priorities

## ⚙️ Configuration

### Environment Variables

```bash
GEMINI_API_KEY=your_key_here  # Required for AI generation
```

### Code Options

```python
# Force Gemini (will fail if no API key)
generator = GeminiDataGenerator(...)

# Force templates (no AI)
from data_generator import DataGenerator
generator = DataGenerator(...)
```

## 🛡️ Error Handling

The system handles:
- ✅ Missing API key → Falls back to templates
- ✅ API errors → Falls back to templates
- ✅ Rate limits → Falls back to templates
- ✅ Invalid responses → Falls back to templates
- ✅ Network issues → Falls back to templates

**No errors, just graceful degradation!**

## 💡 Benefits

### With Gemini AI:
- More diverse activities
- Better descriptions
- Context-aware generation
- Easy to scale
- Customizable via prompts

### Without Gemini (Templates):
- Fast generation
- No API dependency
- Consistent results
- Works offline
- No costs

## 🔍 Verification

Check if Gemini is being used:

```bash
# Look for this in output:
🤖 Generating activities with Gemini AI...
✅ Generated X activities with Gemini AI
```

Or check API response:
```json
{
  "method": "Gemini AI",
  "activities": 105
}
```

## 📝 Files Changed

- ✅ `data_generator_gemini.py` - New Gemini-powered generator
- ✅ `main.py` - Updated to use Gemini
- ✅ `api.py` - Updated API endpoint
- ✅ `frontend/src/App.tsx` - Added Gemini option
- ✅ `frontend/src/components/ConfigPanel.tsx` - Added checkbox
- ✅ `requirements.txt` - Added google-generativeai

## 🎯 Next Steps

1. Get your API key
2. Set it as environment variable
3. Run the system
4. Enjoy AI-generated activities!

---

**Questions?** Check `GEMINI_SETUP.md` for detailed setup instructions.
