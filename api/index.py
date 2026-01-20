"""
Main API handler for Vercel - routes requests to appropriate handlers
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def handler(req):
    """
    Main handler for Vercel serverless functions.
    Routes requests based on path.
    """
    try:
        # Get path from request
        path_str = getattr(req, 'path', '') or getattr(req, 'url', '/api/health')
        path = path_str.strip('/').split('/')
        
        # Get the endpoint name (e.g., /api/health -> health)
        endpoint = path[-1] if path else 'health'
    
    # Route to appropriate handler
    if endpoint == 'health':
        from health import handler as health_handler
        return health_handler(req)
    elif endpoint == 'generate-data':
        from generate_data import handler as generate_data_handler
        return generate_data_handler(req)
    elif endpoint == 'generate-schedule':
        from generate_schedule import handler as generate_schedule_handler
        return generate_schedule_handler(req)
    elif endpoint == 'schedule':
        from schedule import handler as schedule_handler
        return schedule_handler(req)
    elif endpoint == 'statistics':
        from statistics import handler as statistics_handler
        return statistics_handler(req)
    elif endpoint == 'download':
        from download import handler as download_handler
        return download_handler(req)
    elif endpoint == 'activities':
        from activities import handler as activities_handler
        return activities_handler(req)
    else:
        return {
            'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({"error": "Endpoint not found"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "error": "Internal server error",
                "message": str(e)
            })
        }
