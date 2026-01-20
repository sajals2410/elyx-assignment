# Gemini API Setup Guide

## 🤖 Using Gemini AI for Data Generation

The Resource Allocator now supports AI-powered data generation using Google's Gemini API. This generates more diverse and realistic health activities compared to template-based generation.

## 📋 Setup Instructions

### Step 1: Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 2: Set the API Key

**Option A: Environment Variable (Recommended)**
```bash
export GEMINI_API_KEY='your_api_key_here'
```

**Option B: Create .env File**
```bash
# Create .env file in project root
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Option C: Set in Terminal Session**
```bash
export GEMINI_API_KEY='your_api_key_here'
python main.py
```

### Step 3: Verify Installation

```bash
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate
python -c "import google.generativeai as genai; print('✅ Gemini API installed')"
```

## 🚀 Usage

### Command Line

**With Gemini AI (if API key set):**
```bash
export GEMINI_API_KEY='your_key'
python main.py --weeks 2
```

**Force template-based (no AI):**
```bash
# Just don't set the API key, or modify main.py to set use_gemini=False
python main.py --weeks 2
```

### Python Code

```python
from data_generator_gemini import GeminiDataGenerator

# Will use Gemini if API key is set
generator = GeminiDataGenerator(
    start_date="2026-01-15",
    duration_months=3
)
data = generator.save_all_data("data")
```

### API Endpoint

The Flask API automatically uses Gemini if the API key is available:

```bash
curl -X POST http://localhost:5001/api/generate-data \
  -H "Content-Type: application/json" \
  -d '{"start_date": "2026-01-15", "duration_months": 3, "use_gemini": true}'
```

## ✨ Benefits of Gemini AI Generation

1. **More Diverse Activities**: AI generates unique, varied activities
2. **Realistic Details**: Better descriptions and parameters
3. **Context-Aware**: Understands health and fitness context
4. **Scalable**: Easy to generate more activities
5. **Customizable**: Can adjust prompts for different needs

## 🔄 Fallback Behavior

If Gemini API key is not set or API fails:
- Automatically falls back to template-based generation
- System continues to work normally
- No errors, just uses original method

## 💡 Example Generated Activities

With Gemini AI, you might get activities like:
- "Functional Movement Pattern Training"
- "Metabolic Conditioning Circuit"
- "Recovery Yoga Flow"
- "Nutrition Timing Optimization"
- "Sleep Hygiene Protocol"

These are more diverse than template-based activities.

## 🛠️ Troubleshooting

### API Key Not Working
- Verify key is correct
- Check if key has proper permissions
- Ensure no extra spaces in key

### Rate Limits
- Free tier has rate limits
- If hit limit, falls back to templates
- Consider upgrading for production

### API Errors
- Check internet connection
- Verify API key is active
- Check Google Cloud Console for quotas

## 📝 Notes

- **Free Tier**: Gemini API has a generous free tier
- **Rate Limits**: Be aware of API rate limits
- **Cost**: Free tier should be sufficient for testing
- **Privacy**: Activities are generated, no personal data sent

## 🔐 Security

- Never commit API keys to git
- Use environment variables
- Add `.env` to `.gitignore`
- Rotate keys if exposed

---

**Ready to use!** Set your API key and start generating AI-powered health activities! 🚀
