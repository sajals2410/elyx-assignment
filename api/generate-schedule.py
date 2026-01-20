"""
Generate schedule endpoint for Vercel serverless function
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scheduler import ResourceAllocator, load_data
from calendar_output import CalendarFormatter, generate_all_outputs

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
        weeks = body.get('weeks', 2)
        
        # Calculate end date
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(weeks=weeks)
        end_date = end.strftime("%Y-%m-%d")
        
        # Use /tmp for data and output directories
        data_dir = Path('/tmp/data')
        output_dir = Path('/tmp/output')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load data
        activities, equipment, specialists, allied_health, travel_plans, client_schedule = load_data(str(data_dir))
        
        # Create scheduler
        scheduler = ResourceAllocator(
            activities=activities,
            equipment=equipment,
            specialists=specialists,
            allied_health=allied_health,
            travel_plans=travel_plans,
            client_schedule=client_schedule,
            start_date=start_date,
            end_date=end_date
        )
        
        # Generate schedule
        scheduled_activities = scheduler.generate_schedule()
        statistics = scheduler.get_statistics()
        
        # Generate output files (to /tmp/output)
        generate_all_outputs(scheduled_activities, str(output_dir))
        
        # Convert scheduled activities to JSON-serializable format
        schedule_data = [act.to_dict() for act in scheduled_activities]
        
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
                "schedule": schedule_data,
                "statistics": statistics,
                "total_activities": len(scheduled_activities)
            })
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                "success": False,
                "error": str(e),
                "details": error_details
            })
        }
