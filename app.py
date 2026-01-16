"""
Streamlit App for Resource Allocator - Health Activity Scheduler
A user-friendly frontend for the Resource Allocator system.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

# Import our modules
from data_generator import DataGenerator
from scheduler import ResourceAllocator, load_data
from calendar_output import CalendarFormatter, generate_all_outputs

# Page configuration
st.set_page_config(
    page_title="Resource Allocator",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'schedule_generated' not in st.session_state:
        st.session_state.schedule_generated = False
    if 'scheduled_activities' not in st.session_state:
        st.session_state.scheduled_activities = []
    if 'scheduler' not in st.session_state:
        st.session_state.scheduler = None
    if 'statistics' not in st.session_state:
        st.session_state.statistics = {}


def generate_data_if_needed(start_date: str, duration_months: int):
    """Generate test data if it doesn't exist or is outdated."""
    data_dir = Path("data")
    activities_file = data_dir / "activities.json"
    
    if not activities_file.exists():
        with st.spinner("Generating test data... This may take a moment."):
            generator = DataGenerator(
                start_date=start_date,
                duration_months=duration_months
            )
            generator.save_all_data("data")
        st.success("✓ Test data generated successfully!")
        return True
    return False


def main():
    """Main Streamlit app."""
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🏥 Resource Allocator</h1>', unsafe_allow_html=True)
    st.markdown("### Transform Health Recommendations into Personalized Schedules")
    st.markdown("---")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Date settings
        st.subheader("📅 Schedule Settings")
        start_date = st.date_input(
            "Start Date",
            value=datetime(2026, 1, 15),
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2030, 12, 31)
        )
        
        weeks = st.slider(
            "Number of Weeks",
            min_value=1,
            max_value=24,
            value=2,
            help="How many weeks to schedule"
        )
        
        # Data generation options
        st.subheader("📊 Data Management")
        regenerate_data = st.checkbox(
            "Regenerate Test Data",
            value=False,
            help="Generate fresh test data (activities, equipment, etc.)"
        )
        
        duration_months = st.slider(
            "Data Duration (Months)",
            min_value=1,
            max_value=6,
            value=3,
            help="How many months of availability data to generate"
        )
        
        # Action button
        st.markdown("---")
        generate_button = st.button(
            "🚀 Generate Schedule",
            type="primary",
            use_container_width=True
        )
        
        # Info
        st.markdown("---")
        st.info("""
        **How it works:**
        1. Configure your schedule settings
        2. Click "Generate Schedule"
        3. View results and download outputs
        """)


    # Main content area
    if generate_button:
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date = start_date + timedelta(weeks=weeks)
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # Generate data if needed
        if regenerate_data:
            with st.spinner("🔄 Regenerating test data..."):
                generator = DataGenerator(
                    start_date=start_date_str,
                    duration_months=duration_months
                )
                generator.save_all_data("data")
            st.success("✓ Test data regenerated!")
        
        # Check if data exists
        if not Path("data/activities.json").exists():
            generate_data_if_needed(start_date_str, duration_months)
        
        # Run scheduler
        with st.spinner("📅 Generating personalized schedule... This may take a moment."):
            try:
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
                    start_date=start_date_str,
                    end_date=end_date_str
                )
                
                # Generate schedule
                scheduled_activities = scheduler.generate_schedule()
                statistics = scheduler.get_statistics()
                
                # Store in session state
                st.session_state.schedule_generated = True
                st.session_state.scheduled_activities = scheduled_activities
                st.session_state.scheduler = scheduler
                st.session_state.statistics = statistics
                
                # Generate output files
                with st.spinner("📄 Generating output files..."):
                    generate_all_outputs(scheduled_activities, "output")
                
                st.success(f"✅ Schedule generated successfully! {len(scheduled_activities)} activities scheduled.")
                
            except Exception as e:
                st.error(f"❌ Error generating schedule: {str(e)}")
                st.exception(e)
    
    # Display results if schedule is generated
    if st.session_state.schedule_generated:
        st.markdown("---")
        st.header("📊 Schedule Statistics")
        
        stats = st.session_state.statistics
        scheduled = st.session_state.scheduled_activities
        
        # Statistics columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Activities", stats.get('total_scheduled', 0))
        
        with col2:
            backup_count = stats.get('backup_activities_used', 0)
            st.metric("Backup Activities", backup_count)
        
        with col3:
            date_range = stats.get('date_range', {})
            days = (datetime.strptime(date_range.get('end', start_date_str), "%Y-%m-%d") - 
                   datetime.strptime(date_range.get('start', start_date_str), "%Y-%m-%d")).days
            st.metric("Days Scheduled", days)
        
        with col4:
            by_type = stats.get('by_type', {})
            total = sum(by_type.values())
            st.metric("Activity Types", len(by_type))
        
        # Activity breakdown
        st.subheader("📈 Activity Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # By type chart
            if stats.get('by_type'):
                type_df = pd.DataFrame([
                    {"Type": k.title(), "Count": v}
                    for k, v in stats['by_type'].items()
                ])
                st.bar_chart(type_df.set_index("Type"))
        
        with col2:
            # By priority chart
            if stats.get('by_priority'):
                priority_df = pd.DataFrame([
                    {"Priority": k.title(), "Count": v}
                    for k, v in stats['by_priority'].items()
                ])
                st.bar_chart(priority_df.set_index("Priority"))
        
        # Detailed statistics table
        st.subheader("📋 Detailed Statistics")
        
        stats_data = {
            "Metric": [
                "Total Activities Scheduled",
                "Activities by Type",
                "Activities by Priority",
                "Backup Activities Used",
                "Date Range"
            ],
            "Value": [
                stats.get('total_scheduled', 0),
                str(stats.get('by_type', {})),
                str(stats.get('by_priority', {})),
                stats.get('backup_activities_used', 0),
                f"{stats.get('date_range', {}).get('start', 'N/A')} to {stats.get('date_range', {}).get('end', 'N/A')}"
            ]
        }
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
        
        # Schedule preview
        st.markdown("---")
        st.header("📅 Schedule Preview")
        
        # Date selector
        if scheduled:
            dates = sorted(set(act.scheduled_date for act in scheduled))
            selected_date = st.selectbox(
                "Select Date to View",
                options=dates[:10],  # Show first 10 dates
                index=0
            )
            
            # Show activities for selected date
            day_activities = [act for act in scheduled if act.scheduled_date == selected_date]
            day_activities.sort(key=lambda x: x.scheduled_time)
            
            if day_activities:
                st.subheader(f"Schedule for {selected_date}")
                
                # Create a dataframe for the day
                day_data = []
                for act in day_activities:
                    day_data.append({
                        "Time": f"{act.scheduled_time} - {act.end_time}",
                        "Activity": act.activity.name,
                        "Type": act.activity.activity_type.value.title(),
                        "Duration": f"{act.activity.duration_minutes} min",
                        "Location": act.activity.location,
                        "Backup": "Yes" if act.is_backup else "No"
                    })
                
                day_df = pd.DataFrame(day_data)
                st.dataframe(day_df, use_container_width=True, hide_index=True)
                
                # Show details
                with st.expander("View Activity Details"):
                    for act in day_activities:
                        emoji_map = {
                            "fitness": "🏃",
                            "food": "🥗",
                            "medication": "💊",
                            "therapy": "🧘",
                            "consultation": "👨‍⚕️"
                        }
                        emoji = emoji_map.get(act.activity.activity_type.value, "📌")
                        
                        st.markdown(f"""
                        **{emoji} {act.activity.name}** ({act.scheduled_time} - {act.end_time})
                        - **Type**: {act.activity.activity_type.value.title()}
                        - **Duration**: {act.activity.duration_minutes} minutes
                        - **Details**: {act.activity.details}
                        - **Location**: {act.activity.location}
                        - **Facilitator**: {act.activity.facilitator}
                        """)
                        if act.notes:
                            st.info(f"📝 Notes: {act.notes}")
                        if act.is_backup:
                            st.warning("⚠️ This is a backup activity")
                        st.markdown("---")
            else:
                st.info(f"No activities scheduled for {selected_date}")
        
        # Download section
        st.markdown("---")
        st.header("💾 Download Outputs")
        
        col1, col2, col3, col4 = st.columns(4)
        
        output_dir = Path("output")
        
        with col1:
            if (output_dir / "schedule_text.txt").exists():
                with open(output_dir / "schedule_text.txt", "r") as f:
                    st.download_button(
                        "📄 Download Text Calendar",
                        f.read(),
                        "schedule_text.txt",
                        "text/plain"
                    )
        
        with col2:
            if (output_dir / "schedule.html").exists():
                with open(output_dir / "schedule.html", "r") as f:
                    st.download_button(
                        "🌐 Download HTML Calendar",
                        f.read(),
                        "schedule.html",
                        "text/html"
                    )
        
        with col3:
            if (output_dir / "schedule.ics").exists():
                with open(output_dir / "schedule.ics", "r") as f:
                    st.download_button(
                        "📅 Download iCalendar (.ics)",
                        f.read(),
                        "schedule.ics",
                        "text/calendar"
                    )
        
        with col4:
            if (output_dir / "schedule_summary.json").exists():
                with open(output_dir / "schedule_summary.json", "r") as f:
                    st.download_button(
                        "📊 Download JSON Summary",
                        f.read(),
                        "schedule_summary.json",
                        "application/json"
                    )
        
        # View HTML in iframe
        st.markdown("---")
        st.header("👀 View HTML Calendar")
        
        if (output_dir / "schedule.html").exists():
            html_file = output_dir / "schedule.html"
            with open(html_file, "r") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=800, scrolling=True)
        else:
            st.info("HTML calendar not yet generated. Generate a schedule first.")
    
    else:
        # Welcome message
        st.info("""
        👋 **Welcome to Resource Allocator!**
        
        Configure your schedule settings in the sidebar and click "Generate Schedule" to get started.
        
        The system will:
        1. Load or generate test data (activities, equipment, specialists)
        2. Create a personalized schedule respecting all constraints
        3. Generate multiple output formats (Text, HTML, iCal, JSON)
        """)


if __name__ == "__main__":
    main()
