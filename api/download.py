"""
Download file endpoint for Vercel serverless function
"""

import json
import sys
import os
import base64
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def handler(req):
    """Vercel serverless function handler."""
    # Handle CORS preflight
    if req.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': ''
        }
    
    try:
        # Get file type from query string or path
        file_type = req.path.split('/')[-1] if hasattr(req, 'path') and req.path else None
        if not file_type:
            # Try to get from query string
            query_params = getattr(req, 'query', {}) or {}
            file_type = query_params.get('type')
        
        file_map = {
            'text': 'schedule_text.txt',
            'html': 'schedule.html',
            'ics': 'schedule.ics',
            'json': 'schedule_summary.json'
        }
        
        if file_type not in file_map:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "Invalid file type"})
            }
        
        output_dir = Path('/tmp/output')
        file_path = output_dir / file_map[file_type]
        
        if not file_path.exists():
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({"error": "File not found"})
            }
        
        # Read file and return as base64 or text
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Determine content type
        content_types = {
            'text': 'text/plain',
            'html': 'text/html',
            'ics': 'text/calendar',
            'json': 'application/json'
        }
        
        # Return file as base64 encoded data URL
        file_base64 = base64.b64encode(file_content).decode('utf-8')
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                "success": True,
                "filename": file_map[file_type],
                "content": file_base64,
                "contentType": content_types.get(file_type, 'application/octet-stream')
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
