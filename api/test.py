"""
Simple test endpoint to verify Vercel Python functions work
"""

import json

def handler(req):
    """Simple test handler."""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            "status": "ok",
            "message": "Python function is working!"
        })
    }
