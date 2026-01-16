"""
Flask API backend for Resource Allocator
Provides REST endpoints for the React frontend
"""

from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# Import our modules
from data_generator import DataGenerator
from scheduler import ResourceAllocator, load_data
from calendar_output import CalendarFormatter, generate_all_outputs

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "message": "Resource Allocator API is running"})

@app.route('/api/generate-data', methods=['POST'])
def generate_data():
    """Generate test data."""
    try:
        data = request.json
        start_date = data.get('start_date', '2026-01-15')
        duration_months = data.get('duration_months', 3)
        
        generator = DataGenerator(
            start_date=start_date,
            duration_months=duration_months
        )
        result = generator.save_all_data("data")
        
        return jsonify({
            "success": True,
            "message": "Data generated successfully",
            "activities": len(result['activities']),
            "equipment": len(result['equipment']),
            "specialists": len(result['specialists']),
            "allied_health": len(result['allied_health']),
            "travel_plans": len(result['travel_plans'])
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/generate-schedule', methods=['POST'])
def generate_schedule():
    """Generate a personalized schedule."""
    try:
        data = request.json
        start_date = data.get('start_date', '2026-01-15')
        weeks = data.get('weeks', 2)
        
        # Calculate end date
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = start + timedelta(weeks=weeks)
        end_date = end.strftime("%Y-%m-%d")
        
        # Load data
        activities, equipment, specialists, allied_health, travel_plans, client_schedule = load_data("data")
        
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
        
        # Generate output files
        generate_all_outputs(scheduled_activities, "output")
        
        # Convert scheduled activities to JSON-serializable format
        schedule_data = [act.to_dict() for act in scheduled_activities]
        
        return jsonify({
            "success": True,
            "schedule": schedule_data,
            "statistics": statistics,
            "total_activities": len(scheduled_activities)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/schedule', methods=['GET'])
def get_schedule():
    """Get the current schedule from JSON file."""
    try:
        summary_file = Path("output/schedule_summary.json")
        if not summary_file.exists():
            return jsonify({"success": False, "error": "No schedule found. Generate one first."}), 404
        
        with open(summary_file, 'r') as f:
            data = json.load(f)
        
        return jsonify({
            "success": True,
            "data": data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get schedule statistics."""
    try:
        summary_file = Path("output/schedule_summary.json")
        if not summary_file.exists():
            return jsonify({"success": False, "error": "No schedule found"}), 404
        
        with open(summary_file, 'r') as f:
            data = json.load(f)
        
        return jsonify({
            "success": True,
            "statistics": data.get("statistics", {})
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/download/<file_type>', methods=['GET'])
def download_file(file_type):
    """Download output files."""
    file_map = {
        'text': 'output/schedule_text.txt',
        'html': 'output/schedule.html',
        'ics': 'output/schedule.ics',
        'json': 'output/schedule_summary.json'
    }
    
    if file_type not in file_map:
        return jsonify({"error": "Invalid file type"}), 400
    
    file_path = Path(file_map[file_type])
    if not file_path.exists():
        return jsonify({"error": "File not found"}), 404
    
    return send_file(file_path, as_attachment=True)

@app.route('/api/activities', methods=['GET'])
def get_activities():
    """Get list of all activities."""
    try:
        activities_file = Path("data/activities.json")
        if not activities_file.exists():
            return jsonify({"success": False, "error": "Activities file not found"}), 404
        
        with open(activities_file, 'r') as f:
            activities = json.load(f)
        
        return jsonify({
            "success": True,
            "activities": activities,
            "count": len(activities)
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
