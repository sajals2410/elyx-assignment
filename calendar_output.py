"""
calendar_output.py - Calendar Output Formatter for Resource Allocator

This module generates readable calendar outputs from the scheduled activities.
It supports multiple output formats:
1. Text-based calendar (terminal/console display)
2. HTML calendar (for viewing in a browser)
3. iCalendar format (.ics file for importing into calendar apps)
4. JSON summary (for programmatic use)

The output is designed to be clear and actionable, showing:
- Daily schedules with times and activity details
- Weekly views with summary statistics
- Monthly overviews
- Color-coded activity types
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
from models import ScheduledActivity, ActivityType


# Color codes for terminal output
class Colors:
    """ANSI color codes for terminal output."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"


# Activity type to color mapping
TYPE_COLORS = {
    ActivityType.FITNESS: Colors.GREEN,
    ActivityType.FOOD: Colors.YELLOW,
    ActivityType.MEDICATION: Colors.RED,
    ActivityType.THERAPY: Colors.MAGENTA,
    ActivityType.CONSULTATION: Colors.CYAN,
}

# Activity type to emoji mapping for HTML output
TYPE_EMOJIS = {
    ActivityType.FITNESS: "🏃",
    ActivityType.FOOD: "🥗",
    ActivityType.MEDICATION: "💊",
    ActivityType.THERAPY: "🧘",
    ActivityType.CONSULTATION: "👨‍⚕️",
}


class CalendarFormatter:
    """
    Generates formatted calendar outputs from scheduled activities.
    
    This class takes the output from the ResourceAllocator scheduler
    and produces various calendar formats for easy viewing and integration.
    """
    
    def __init__(self, scheduled_activities: List[ScheduledActivity]):
        """
        Initialize the calendar formatter.
        
        Args:
            scheduled_activities: List of scheduled activities from the scheduler
        """
        self.activities = scheduled_activities
        self._organize_by_date()
    
    def _organize_by_date(self):
        """Organize activities by date for easy access."""
        self.by_date = defaultdict(list)
        for activity in self.activities:
            self.by_date[activity.scheduled_date].append(activity)
        
        # Sort each day by time
        for date in self.by_date:
            self.by_date[date].sort(key=lambda x: x.scheduled_time)
    
    def generate_text_calendar(self, start_date: str = None, end_date: str = None,
                               use_colors: bool = True) -> str:
        """
        Generate a text-based calendar view.
        
        Args:
            start_date: Optional start date filter (YYYY-MM-DD)
            end_date: Optional end date filter (YYYY-MM-DD)
            use_colors: Whether to use ANSI colors in output
            
        Returns:
            Formatted text string representing the calendar
        """
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append(" " * 25 + "📅 PERSONALIZED HEALTH SCHEDULE 📅")
        lines.append("=" * 80)
        lines.append("")
        
        # Get date range
        all_dates = sorted(self.by_date.keys())
        if not all_dates:
            return "No activities scheduled."
        
        if start_date:
            all_dates = [d for d in all_dates if d >= start_date]
        if end_date:
            all_dates = [d for d in all_dates if d <= end_date]
        
        # Group by week
        current_week = None
        week_activities = []
        
        for date_str in all_dates:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            week_num = date.isocalendar()[1]
            year = date.year
            week_key = f"{year}-W{week_num:02d}"
            
            if week_key != current_week:
                # Print previous week summary if exists
                if current_week and week_activities:
                    lines.append(self._format_week_summary(week_activities, use_colors))
                
                current_week = week_key
                week_activities = []
                lines.append("")
                week_header = f"📆 WEEK {week_num}, {year}"
                if use_colors:
                    lines.append(f"{Colors.BOLD}{week_header}{Colors.RESET}")
                else:
                    lines.append(week_header)
                lines.append("-" * 80)
            
            # Format the day
            day_str = self._format_day(date_str, self.by_date[date_str], use_colors)
            lines.append(day_str)
            week_activities.extend(self.by_date[date_str])
        
        # Final week summary
        if week_activities:
            lines.append(self._format_week_summary(week_activities, use_colors))
        
        lines.append("")
        lines.append("=" * 80)
        lines.append(" " * 30 + "END OF SCHEDULE")
        lines.append("=" * 80)
        
        return "\n".join(lines)
    
    def _format_day(self, date_str: str, activities: List[ScheduledActivity],
                    use_colors: bool) -> str:
        """Format a single day's schedule."""
        lines = []
        date = datetime.strptime(date_str, "%Y-%m-%d")
        day_name = date.strftime("%A")
        formatted_date = date.strftime("%B %d, %Y")
        
        header = f"\n  📅 {day_name}, {formatted_date}"
        if use_colors:
            lines.append(f"{Colors.BOLD}{header}{Colors.RESET}")
        else:
            lines.append(header)
        
        if not activities:
            lines.append("    (No activities scheduled)")
            return "\n".join(lines)
        
        for act in activities:
            emoji = TYPE_EMOJIS.get(act.activity.activity_type, "📌")
            time_str = f"{act.scheduled_time}-{act.end_time}"
            name = act.activity.name
            details = act.activity.details[:50] + "..." if len(act.activity.details) > 50 else act.activity.details
            
            if use_colors:
                color = TYPE_COLORS.get(act.activity.activity_type, Colors.WHITE)
                activity_line = f"    {time_str} {emoji} {color}{name}{Colors.RESET}"
            else:
                activity_line = f"    {time_str} {emoji} {name}"
            
            lines.append(activity_line)
            
            if details:
                lines.append(f"             └─ {details}")
            
            if act.notes:
                lines.append(f"             📝 {act.notes}")
            
            if act.is_backup:
                lines.append(f"             ⚠️  (Backup activity)")
        
        return "\n".join(lines)
    
    def _format_week_summary(self, activities: List[ScheduledActivity],
                             use_colors: bool) -> str:
        """Generate a week summary."""
        by_type = defaultdict(int)
        total_minutes = 0
        
        for act in activities:
            by_type[act.activity.activity_type.value] += 1
            total_minutes += act.activity.duration_minutes
        
        lines = []
        lines.append("")
        lines.append("  📊 Week Summary:")
        
        for act_type, count in sorted(by_type.items()):
            emoji = TYPE_EMOJIS.get(ActivityType(act_type), "📌")
            lines.append(f"     {emoji} {act_type.title()}: {count} activities")
        
        hours = total_minutes // 60
        mins = total_minutes % 60
        lines.append(f"     ⏱️  Total scheduled time: {hours}h {mins}m")
        
        return "\n".join(lines)
    
    def generate_html_calendar(self, output_file: str = "schedule.html") -> str:
        """
        Generate an HTML calendar view.
        
        Args:
            output_file: Path to save the HTML file
            
        Returns:
            The HTML content as a string
        """
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personalized Health Schedule</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        header {
            text-align: center;
            color: white;
            padding: 30px 0;
        }
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        .legend {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 15px;
            margin: 20px 0;
        }
        .legend-item {
            background: white;
            padding: 8px 15px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.9em;
        }
        .week {
            background: white;
            border-radius: 15px;
            margin: 20px 0;
            overflow: hidden;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }
        .week-header {
            background: linear-gradient(135deg, #5c6bc0 0%, #7e57c2 100%);
            color: white;
            padding: 15px 25px;
            font-size: 1.3em;
        }
        .day {
            border-bottom: 1px solid #eee;
        }
        .day:last-child {
            border-bottom: none;
        }
        .day-header {
            background: #f8f9fa;
            padding: 12px 25px;
            font-weight: 600;
            color: #333;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .day-count {
            font-size: 0.85em;
            color: #666;
        }
        .activities {
            padding: 10px 25px;
        }
        .activity {
            display: flex;
            padding: 12px 0;
            border-bottom: 1px dashed #eee;
            align-items: flex-start;
        }
        .activity:last-child {
            border-bottom: none;
        }
        .activity-time {
            min-width: 110px;
            font-weight: 600;
            color: #555;
            font-size: 0.9em;
        }
        .activity-emoji {
            font-size: 1.3em;
            margin-right: 12px;
        }
        .activity-content {
            flex: 1;
        }
        .activity-name {
            font-weight: 600;
            color: #333;
            margin-bottom: 4px;
        }
        .activity-details {
            font-size: 0.85em;
            color: #666;
        }
        .activity-notes {
            font-size: 0.8em;
            color: #888;
            font-style: italic;
            margin-top: 4px;
        }
        .fitness { border-left: 4px solid #4CAF50; padding-left: 12px; }
        .food { border-left: 4px solid #FF9800; padding-left: 12px; }
        .medication { border-left: 4px solid #f44336; padding-left: 12px; }
        .therapy { border-left: 4px solid #9C27B0; padding-left: 12px; }
        .consultation { border-left: 4px solid #00BCD4; padding-left: 12px; }
        .week-summary {
            background: #f8f9fa;
            padding: 20px 25px;
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 15px;
        }
        .summary-item {
            text-align: center;
        }
        .summary-item .count {
            font-size: 1.5em;
            font-weight: 700;
            color: #5c6bc0;
        }
        .summary-item .label {
            font-size: 0.8em;
            color: #666;
        }
        .backup-badge {
            background: #FFE0B2;
            color: #E65100;
            font-size: 0.7em;
            padding: 2px 8px;
            border-radius: 10px;
            margin-left: 10px;
        }
        @media (max-width: 600px) {
            .activity {
                flex-direction: column;
            }
            .activity-time {
                margin-bottom: 5px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📅 Personalized Health Schedule</h1>
            <p>Your optimized wellness plan from the Resource Allocator</p>
        </header>
        
        <div class="legend">
            <div class="legend-item"><span>🏃</span> Fitness</div>
            <div class="legend-item"><span>🥗</span> Food/Nutrition</div>
            <div class="legend-item"><span>💊</span> Medication</div>
            <div class="legend-item"><span>🧘</span> Therapy</div>
            <div class="legend-item"><span>👨‍⚕️</span> Consultation</div>
        </div>
"""
        
        # Group by week
        weeks = defaultdict(lambda: defaultdict(list))
        for act in self.activities:
            date = datetime.strptime(act.scheduled_date, "%Y-%m-%d")
            week_num = date.isocalendar()[1]
            year = date.year
            week_key = f"{year}-W{week_num:02d}"
            weeks[week_key][act.scheduled_date].append(act)
        
        for week_key in sorted(weeks.keys()):
            week_data = weeks[week_key]
            total_activities = sum(len(acts) for acts in week_data.values())
            total_minutes = sum(act.activity.duration_minutes for acts in week_data.values() for act in acts)
            
            html += f"""
        <div class="week">
            <div class="week-header">📆 Week {week_key.split('-W')[1]}, {week_key.split('-W')[0]} ({total_activities} activities)</div>
"""
            
            for date_str in sorted(week_data.keys()):
                activities = sorted(week_data[date_str], key=lambda x: x.scheduled_time)
                date = datetime.strptime(date_str, "%Y-%m-%d")
                day_name = date.strftime("%A")
                formatted_date = date.strftime("%B %d")
                
                html += f"""
            <div class="day">
                <div class="day-header">
                    <span>{day_name}, {formatted_date}</span>
                    <span class="day-count">{len(activities)} activities</span>
                </div>
                <div class="activities">
"""
                
                for act in activities:
                    emoji = TYPE_EMOJIS.get(act.activity.activity_type, "📌")
                    type_class = act.activity.activity_type.value
                    backup_badge = '<span class="backup-badge">BACKUP</span>' if act.is_backup else ''
                    
                    html += f"""
                    <div class="activity {type_class}">
                        <div class="activity-time">{act.scheduled_time} - {act.end_time}</div>
                        <div class="activity-emoji">{emoji}</div>
                        <div class="activity-content">
                            <div class="activity-name">{act.activity.name}{backup_badge}</div>
                            <div class="activity-details">{act.activity.details}</div>
"""
                    if act.notes:
                        html += f'                            <div class="activity-notes">📝 {act.notes}</div>\n'
                    
                    html += """                        </div>
                    </div>
"""
                
                html += """                </div>
            </div>
"""
            
            # Week summary
            by_type = defaultdict(int)
            for acts in week_data.values():
                for act in acts:
                    by_type[act.activity.activity_type.value] += 1
            
            hours = total_minutes // 60
            mins = total_minutes % 60
            
            html += f"""
            <div class="week-summary">
                <div class="summary-item">
                    <div class="count">{by_type.get('fitness', 0)}</div>
                    <div class="label">🏃 Fitness</div>
                </div>
                <div class="summary-item">
                    <div class="count">{by_type.get('food', 0)}</div>
                    <div class="label">🥗 Nutrition</div>
                </div>
                <div class="summary-item">
                    <div class="count">{by_type.get('medication', 0)}</div>
                    <div class="label">💊 Medication</div>
                </div>
                <div class="summary-item">
                    <div class="count">{by_type.get('therapy', 0)}</div>
                    <div class="label">🧘 Therapy</div>
                </div>
                <div class="summary-item">
                    <div class="count">{by_type.get('consultation', 0)}</div>
                    <div class="label">👨‍⚕️ Consultations</div>
                </div>
                <div class="summary-item">
                    <div class="count">{hours}h {mins}m</div>
                    <div class="label">⏱️ Total Time</div>
                </div>
            </div>
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        return html
    
    def generate_icalendar(self, output_file: str = "schedule.ics") -> str:
        """
        Generate an iCalendar (.ics) file for importing into calendar apps.
        
        Args:
            output_file: Path to save the .ics file
            
        Returns:
            The iCalendar content as a string
        """
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Resource Allocator//Health Schedule//EN",
            "CALSCALE:GREGORIAN",
            "METHOD:PUBLISH",
            "X-WR-CALNAME:Health Schedule",
        ]
        
        for i, act in enumerate(self.activities):
            date = datetime.strptime(act.scheduled_date, "%Y-%m-%d")
            start_parts = act.scheduled_time.split(":")
            end_parts = act.end_time.split(":")
            
            start_dt = date.replace(hour=int(start_parts[0]), minute=int(start_parts[1]))
            end_dt = date.replace(hour=int(end_parts[0]), minute=int(end_parts[1]))
            
            uid = f"event-{i}-{start_dt.strftime('%Y%m%d')}@resourceallocator"
            
            emoji = TYPE_EMOJIS.get(act.activity.activity_type, "📌")
            summary = f"{emoji} {act.activity.name}"
            
            description = act.activity.details
            if act.notes:
                description += f"\\n\\nNotes: {act.notes}"
            if act.activity.facilitator:
                description += f"\\n\\nFacilitator: {act.activity.facilitator}"
            if act.activity.metrics_to_collect:
                description += f"\\n\\nMetrics: {', '.join(act.activity.metrics_to_collect)}"
            
            lines.extend([
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}",
                f"DTSTART:{start_dt.strftime('%Y%m%dT%H%M%S')}",
                f"DTEND:{end_dt.strftime('%Y%m%dT%H%M%S')}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                f"LOCATION:{act.activity.location}",
                f"CATEGORIES:{act.activity.activity_type.value.upper()}",
                "END:VEVENT",
            ])
        
        lines.append("END:VCALENDAR")
        
        content = "\r\n".join(lines)
        
        with open(output_file, 'w') as f:
            f.write(content)
        
        return content
    
    def generate_json_summary(self, output_file: str = "schedule_summary.json") -> Dict:
        """
        Generate a JSON summary of the schedule.
        
        Args:
            output_file: Path to save the JSON file
            
        Returns:
            Dictionary containing the schedule summary
        """
        by_date = {}
        for date_str, activities in sorted(self.by_date.items()):
            by_date[date_str] = [act.to_dict() for act in activities]
        
        # Calculate statistics
        total_minutes = sum(act.activity.duration_minutes for act in self.activities)
        by_type = defaultdict(int)
        by_priority = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for act in self.activities:
            by_type[act.activity.activity_type.value] += 1
            p = act.activity.priority
            if p <= 20:
                by_priority["critical"] += 1
            elif p <= 50:
                by_priority["high"] += 1
            elif p <= 80:
                by_priority["medium"] += 1
            else:
                by_priority["low"] += 1
        
        summary = {
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_activities": len(self.activities),
                "total_days": len(self.by_date),
                "total_minutes": total_minutes,
                "total_hours": round(total_minutes / 60, 1),
                "by_type": dict(by_type),
                "by_priority": by_priority,
                "backup_activities": sum(1 for act in self.activities if act.is_backup)
            },
            "schedule": by_date
        }
        
        with open(output_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def print_daily_view(self, date_str: str, use_colors: bool = True):
        """Print a single day's schedule to console."""
        if date_str not in self.by_date:
            print(f"No activities scheduled for {date_str}")
            return
        
        print(self._format_day(date_str, self.by_date[date_str], use_colors))


def generate_all_outputs(scheduled_activities: List[ScheduledActivity], 
                         output_dir: str = "output") -> Dict[str, str]:
    """
    Generate all calendar output formats.
    
    Args:
        scheduled_activities: List of scheduled activities
        output_dir: Directory to save output files
        
    Returns:
        Dictionary mapping output type to file path
    """
    formatter = CalendarFormatter(scheduled_activities)
    
    outputs = {}
    
    # Text calendar
    text_output = formatter.generate_text_calendar(use_colors=False)
    text_file = f"{output_dir}/schedule_text.txt"
    with open(text_file, 'w') as f:
        f.write(text_output)
    outputs["text"] = text_file
    print(f"✓ Text calendar saved to {text_file}")
    
    # HTML calendar
    html_file = f"{output_dir}/schedule.html"
    formatter.generate_html_calendar(html_file)
    outputs["html"] = html_file
    print(f"✓ HTML calendar saved to {html_file}")
    
    # iCalendar
    ics_file = f"{output_dir}/schedule.ics"
    formatter.generate_icalendar(ics_file)
    outputs["ics"] = ics_file
    print(f"✓ iCalendar file saved to {ics_file}")
    
    # JSON summary
    json_file = f"{output_dir}/schedule_summary.json"
    formatter.generate_json_summary(json_file)
    outputs["json"] = json_file
    print(f"✓ JSON summary saved to {json_file}")
    
    return outputs


if __name__ == "__main__":
    # Test with sample data
    from scheduler import load_data, ResourceAllocator
    
    print("Loading data...")
    activities, equipment, specialists, allied_health, travel_plans, client_schedule = load_data("data")
    
    print("Generating schedule...")
    scheduler = ResourceAllocator(
        activities=activities,
        equipment=equipment,
        specialists=specialists,
        allied_health=allied_health,
        travel_plans=travel_plans,
        client_schedule=client_schedule,
        start_date="2026-01-15",
        end_date="2026-02-15"  # One month for testing
    )
    
    scheduled = scheduler.generate_schedule()
    
    print(f"\nGenerated {len(scheduled)} scheduled activities")
    
    # Generate outputs
    print("\nGenerating calendar outputs...")
    outputs = generate_all_outputs(scheduled, "output")
    
    # Print first week to console
    formatter = CalendarFormatter(scheduled)
    print("\n" + "=" * 80)
    print("FIRST WEEK PREVIEW:")
    print("=" * 80)
    print(formatter.generate_text_calendar(start_date="2026-01-15", end_date="2026-01-21", use_colors=True))
