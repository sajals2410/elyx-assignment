"""
Generate data endpoint for Vercel serverless function
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from data_generator import DataGenerator
from data_generator_gemini import GeminiDataGenerator

def handler(req):
    """Vercel serverless function handler."""
    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        # Parse request body
        body = req.json if hasattr(req, 'json') else (json.loads(req.body) if req.body else {})
        start_date = body.get('start_date', '2026-01-15')
        duration_months = body.get('duration_months', 3)
        use_gemini = body.get('use_gemini', True)
        
        # Create data directory if it doesn't exist
        data_dir = Path('/tmp/data')
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if Gemini API key is available
        gemini_api_key = os.getenv('GEMINI_API_KEY', '')
        
        if use_gemini and gemini_api_key:
            generator = GeminiDataGenerator(
                start_date=start_date,
                duration_months=duration_months
            )
            method = "Gemini AI"
        else:
            generator = DataGenerator(
                start_date=start_date,
                duration_months=duration_months
            )
            method = "Template-based"
        
        # Save data to /tmp (Vercel serverless functions have /tmp directory)
        result = generator.save_all_data(str(data_dir))
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                "success": True,
                "message": f"Data generated successfully using {method}",
                "method": method,
                "activities": len(result['activities']),
                "equipment": len(result['equipment']),
                "specialists": len(result['specialists']),
                "allied_health": len(result['allied_health']),
                "travel_plans": len(result['travel_plans'])
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "success": False,
                "error": str(e)
            })
        }
