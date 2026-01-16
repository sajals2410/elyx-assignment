"""
main.py - Resource Allocator Main Entry Point

This is the main entry point for the Resource Allocator system.
It orchestrates the entire workflow:
1. Generate test data (activities and availability schedules)
2. Run the scheduler to create a personalized plan
3. Output the schedule in multiple readable formats

Usage:
    python main.py                    # Run with default settings
    python main.py --generate-only    # Only generate test data
    python main.py --schedule-only    # Only run scheduler (data must exist)
    python main.py --weeks 4          # Generate schedule for 4 weeks

The Resource Allocator system transforms HealthSpan AI recommendations
into actionable, scheduled activities while respecting all constraints
(equipment, specialists, travel, personal schedule).
"""

import os
import sys
import argparse
from datetime import datetime

# Import our modules
from data_generator import DataGenerator
from scheduler import ResourceAllocator, load_data
from calendar_output import CalendarFormatter, generate_all_outputs


def ensure_directories():
    """Ensure required directories exist."""
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    print("✓ Directories created/verified")


def generate_test_data(start_date: str = "2026-01-15", duration_months: int = 3):
    """
    Generate all test data for the Resource Allocator.
    
    This creates:
    - 100+ realistic health activities
    - Equipment availability for 3 months
    - Specialist schedules for 3 months
    - Allied health professional schedules
    - Travel plans
    - Client personal schedule
    
    Args:
        start_date: Start date for the schedules
        duration_months: Number of months to generate
    """
    print("\n" + "=" * 60)
    print("📊 GENERATING TEST DATA")
    print("=" * 60)
    
    generator = DataGenerator(start_date=start_date, duration_months=duration_months)
    data = generator.save_all_data("data")
    
    print(f"\n✓ Generated {len(data['activities'])} activities")
    print(f"✓ Generated {len(data['equipment'])} equipment items with availability")
    print(f"✓ Generated {len(data['specialists'])} specialists with schedules")
    print(f"✓ Generated {len(data['allied_health'])} allied health professionals")
    print(f"✓ Generated {len(data['travel_plans'])} travel plans")
    print(f"✓ Client schedule created")
    
    return data


def run_scheduler(start_date: str = "2026-01-15", weeks: int = 12):
    """
    Run the Resource Allocator scheduler.
    
    This takes the action plan (activities) and all constraints
    to generate an optimized, personalized schedule.
    
    Args:
        start_date: Start date for scheduling
        weeks: Number of weeks to schedule
        
    Returns:
        Tuple of (scheduler, scheduled_activities)
    """
    print("\n" + "=" * 60)
    print("📅 RUNNING RESOURCE ALLOCATOR SCHEDULER")
    print("=" * 60)
    
    # Load data
    print("\nLoading data from files...")
    activities, equipment, specialists, allied_health, travel_plans, client_schedule = load_data("data")
    
    print(f"  → {len(activities)} activities loaded")
    print(f"  → {len(equipment)} equipment items loaded")
    print(f"  → {len(specialists)} specialists loaded")
    print(f"  → {len(allied_health)} allied health professionals loaded")
    print(f"  → {len(travel_plans)} travel plans loaded")
    
    # Calculate end date
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = start + __import__('datetime').timedelta(weeks=weeks)
    end_date = end.strftime("%Y-%m-%d")
    
    print(f"\nScheduling period: {start_date} to {end_date} ({weeks} weeks)")
    
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
    print("\nGenerating personalized schedule...")
    scheduled_activities = scheduler.generate_schedule()
    
    # Print statistics
    stats = scheduler.get_statistics()
    print(f"\n✓ Schedule generated successfully!")
    print(f"  → Total activities scheduled: {stats['total_scheduled']}")
    print(f"  → Activities by type: {stats['by_type']}")
    print(f"  → Activities by priority: {stats['by_priority']}")
    print(f"  → Backup activities used: {stats['backup_activities_used']}")
    
    # Save scheduling log
    with open("output/scheduling_log.txt", "w") as f:
        f.write("\n".join(scheduler.scheduling_log))
    print(f"  → Scheduling log saved to output/scheduling_log.txt")
    
    return scheduler, scheduled_activities


def generate_outputs(scheduled_activities):
    """
    Generate all output formats for the schedule.
    
    Creates:
    - Text calendar (console-friendly)
    - HTML calendar (visual, browser-viewable)
    - iCalendar (.ics) file (for import to calendar apps)
    - JSON summary (for programmatic use)
    
    Args:
        scheduled_activities: List of scheduled activities
    """
    print("\n" + "=" * 60)
    print("📄 GENERATING OUTPUT FILES")
    print("=" * 60)
    
    outputs = generate_all_outputs(scheduled_activities, "output")
    
    print(f"\n✓ All outputs generated in 'output/' directory")
    print(f"  → Text calendar: {outputs['text']}")
    print(f"  → HTML calendar: {outputs['html']}")
    print(f"  → iCalendar file: {outputs['ics']}")
    print(f"  → JSON summary: {outputs['json']}")
    
    return outputs


def print_sample_schedule(scheduled_activities, days: int = 7):
    """
    Print a sample of the schedule to the console.
    
    Args:
        scheduled_activities: List of scheduled activities
        days: Number of days to show
    """
    print("\n" + "=" * 60)
    print(f"📅 SAMPLE SCHEDULE (First {days} days)")
    print("=" * 60)
    
    formatter = CalendarFormatter(scheduled_activities)
    
    # Get date range
    dates = sorted(set(act.scheduled_date for act in scheduled_activities))
    if dates:
        start = dates[0]
        # Find the end date for the sample
        sample_dates = dates[:min(days, len(dates))]
        end = sample_dates[-1] if sample_dates else start
        
        print(formatter.generate_text_calendar(start_date=start, end_date=end, use_colors=True))


def main():
    """Main entry point for the Resource Allocator."""
    parser = argparse.ArgumentParser(
        description="Resource Allocator - Transform health recommendations into scheduled activities"
    )
    parser.add_argument(
        "--generate-only",
        action="store_true",
        help="Only generate test data, don't run scheduler"
    )
    parser.add_argument(
        "--schedule-only",
        action="store_true",
        help="Only run scheduler (assumes data already exists)"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2026-01-15",
        help="Start date for scheduling (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--weeks",
        type=int,
        default=12,
        help="Number of weeks to schedule (default: 12)"
    )
    parser.add_argument(
        "--sample-days",
        type=int,
        default=7,
        help="Number of days to show in console preview (default: 7)"
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Skip the console preview of the schedule"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("🏥 RESOURCE ALLOCATOR - Health Activity Scheduler")
    print("=" * 60)
    print("Transforming HealthSpan AI recommendations into")
    print("personalized, actionable schedules.")
    print("=" * 60)
    
    # Ensure directories exist
    ensure_directories()
    
    # Generate data if needed
    if not args.schedule_only:
        generate_test_data(
            start_date=args.start_date,
            duration_months=max(3, (args.weeks // 4) + 1)
        )
    
    # Run scheduler if needed
    if not args.generate_only:
        scheduler, scheduled = run_scheduler(
            start_date=args.start_date,
            weeks=args.weeks
        )
        
        # Generate outputs
        generate_outputs(scheduled)
        
        # Print sample to console
        if not args.no_preview:
            print_sample_schedule(scheduled, days=args.sample_days)
    
    print("\n" + "=" * 60)
    print("✅ RESOURCE ALLOCATOR COMPLETE")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. View HTML calendar: open output/schedule.html in a browser")
    print("  2. Import to calendar: use output/schedule.ics")
    print("  3. Analyze data: check output/schedule_summary.json")
    print("  4. View full text schedule: cat output/schedule_text.txt")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
