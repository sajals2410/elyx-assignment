"""
scheduler.py - Resource Allocator Scheduler

This module implements the core scheduling algorithm for the Resource Allocator.
It takes the action plan (activities) and all resource availability constraints
to generate a personalized, optimized schedule.

The scheduler works by:
1. Sorting activities by priority (health importance)
2. Determining required instances based on frequency
3. Checking resource availability (equipment, specialists, allied health)
4. Respecting client constraints (travel, work hours, preferences)
5. Assigning time slots and handling conflicts
6. Using backup activities when primary activities cannot be scheduled

Algorithm Overview:
- Priority-based scheduling ensures most important health activities are scheduled first
- Greedy allocation within each day's available time slots
- Constraint satisfaction for resource availability
- Fallback to backup activities or remote options when needed
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional, Set
from collections import defaultdict
from models import (
    Activity, ActivityType, Frequency, TimeSlot, ScheduledActivity,
    Equipment, Specialist, AlliedHealth, TravelPlan, ClientSchedule
)


class ResourceAllocator:
    """
    The main scheduler class that transforms action plans into personalized schedules.
    
    This scheduler coordinates:
    - Activity priorities and frequencies
    - Equipment availability
    - Specialist schedules
    - Allied health professional schedules
    - Client's personal schedule and travel plans
    
    The output is a day-by-day schedule optimized for health outcomes.
    """
    
    def __init__(
        self,
        activities: List[Activity],
        equipment: List[Equipment],
        specialists: List[Specialist],
        allied_health: List[AlliedHealth],
        travel_plans: List[TravelPlan],
        client_schedule: ClientSchedule,
        start_date: str,
        end_date: str
    ):
        """
        Initialize the Resource Allocator with all required data.
        
        Args:
            activities: List of activities from the action plan
            equipment: List of equipment with availability
            specialists: List of specialists with schedules
            allied_health: List of allied health professionals with schedules
            travel_plans: Client's travel commitments
            client_schedule: Client's personal schedule constraints
            start_date: Start date for scheduling (YYYY-MM-DD)
            end_date: End date for scheduling (YYYY-MM-DD)
        """
        self.activities = sorted(activities, key=lambda x: x.priority)  # Sort by priority
        self.equipment = {e.id: e for e in equipment}
        self.specialists = {s.id: s for s in specialists}
        self.allied_health = {ah.id: ah for ah in allied_health}
        self.travel_plans = travel_plans
        self.client_schedule = client_schedule
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        # Build quick lookup structures
        self._build_availability_index()
        self._build_travel_index()
        
        # Track scheduled activities
        self.scheduled_activities: List[ScheduledActivity] = []
        self.scheduling_log: List[str] = []
        
    def _build_availability_index(self):
        """
        Build an index of availability by date for quick lookup.
        
        This creates dictionaries mapping dates to available time slots
        for equipment, specialists, and allied health professionals.
        """
        self.equipment_availability = defaultdict(dict)
        self.specialist_availability = defaultdict(dict)
        self.allied_health_availability = defaultdict(dict)
        
        # Index equipment availability by date
        for eq_id, eq in self.equipment.items():
            for slot in eq.availability_schedule:
                if slot.is_available:
                    self.equipment_availability[slot.date][eq_id] = slot
        
        # Index specialist availability by date
        for spec_id, spec in self.specialists.items():
            for slot in spec.availability_schedule:
                if slot.is_available:
                    if slot.date not in self.specialist_availability:
                        self.specialist_availability[slot.date] = {}
                    if spec_id not in self.specialist_availability[slot.date]:
                        self.specialist_availability[slot.date][spec_id] = []
                    self.specialist_availability[slot.date][spec_id].append(slot)
        
        # Index allied health availability by date
        for ah_id, ah in self.allied_health.items():
            for slot in ah.availability_schedule:
                if slot.is_available:
                    if slot.date not in self.allied_health_availability:
                        self.allied_health_availability[slot.date] = {}
                    if ah_id not in self.allied_health_availability[slot.date]:
                        self.allied_health_availability[slot.date][ah_id] = []
                    self.allied_health_availability[slot.date][ah_id].append(slot)
    
    def _build_travel_index(self):
        """Build an index of travel dates for quick lookup."""
        self.travel_dates: Set[str] = set()
        self.travel_by_date: Dict[str, TravelPlan] = {}
        
        for travel in self.travel_plans:
            start = datetime.strptime(travel.start_date, "%Y-%m-%d")
            end = datetime.strptime(travel.end_date, "%Y-%m-%d")
            current = start
            while current <= end:
                date_str = current.strftime("%Y-%m-%d")
                self.travel_dates.add(date_str)
                self.travel_by_date[date_str] = travel
                current += timedelta(days=1)
    
    def _is_client_available(self, date_str: str, start_time: str, end_time: str) -> bool:
        """
        Check if the client is available at the given time.
        
        Args:
            date_str: Date to check (YYYY-MM-DD)
            start_time: Start time (HH:MM)
            end_time: End time (HH:MM)
            
        Returns:
            True if client is available, False otherwise
        """
        # Check if client is traveling
        if date_str in self.travel_dates:
            # During travel, only remote activities are possible
            return True  # Will be handled separately
        
        # Check against blocked times
        for blocked in self.client_schedule.blocked_times:
            if blocked.date == date_str and not blocked.is_available:
                # Check for time overlap
                if self._times_overlap(start_time, end_time, 
                                       blocked.start_time, blocked.end_time):
                    return False
        
        # Check wake/sleep times
        wake_minutes = self._time_to_minutes(self.client_schedule.wake_time)
        sleep_minutes = self._time_to_minutes(self.client_schedule.sleep_time)
        start_minutes = self._time_to_minutes(start_time)
        end_minutes = self._time_to_minutes(end_time)
        
        if start_minutes < wake_minutes or end_minutes > sleep_minutes:
            return False
        
        return True
    
    def _times_overlap(self, start1: str, end1: str, start2: str, end2: str) -> bool:
        """Check if two time ranges overlap."""
        s1 = self._time_to_minutes(start1)
        e1 = self._time_to_minutes(end1)
        s2 = self._time_to_minutes(start2)
        e2 = self._time_to_minutes(end2)
        return s1 < e2 and s2 < e1
    
    def _time_to_minutes(self, time_str: str) -> int:
        """Convert HH:MM time string to minutes since midnight."""
        parts = time_str.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    
    def _minutes_to_time(self, minutes: int) -> str:
        """Convert minutes since midnight to HH:MM string."""
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours:02d}:{mins:02d}"
    
    def _check_equipment_available(self, activity: Activity, date_str: str) -> bool:
        """Check if all required equipment is available on a date."""
        if not activity.equipment_needed:
            return True
        
        for eq_id in activity.equipment_needed:
            if eq_id not in self.equipment_availability.get(date_str, {}):
                return False
        return True
    
    def _check_specialist_available(self, activity: Activity, date_str: str, 
                                     start_time: str, end_time: str) -> bool:
        """Check if required specialist is available at the given time."""
        if not activity.specialist_needed:
            return True
        
        spec_id = activity.specialist_needed
        if spec_id not in self.specialist_availability.get(date_str, {}):
            return False
        
        # Check if time slot overlaps with specialist's available slots
        for slot in self.specialist_availability[date_str][spec_id]:
            if self._time_within_slot(start_time, end_time, slot):
                return True
        return False
    
    def _check_allied_health_available(self, activity: Activity, date_str: str,
                                        start_time: str, end_time: str) -> bool:
        """Check if required allied health professional is available."""
        if not activity.allied_health_needed:
            return True
        
        ah_id = activity.allied_health_needed
        if ah_id not in self.allied_health_availability.get(date_str, {}):
            return False
        
        for slot in self.allied_health_availability[date_str][ah_id]:
            if self._time_within_slot(start_time, end_time, slot):
                return True
        return False
    
    def _time_within_slot(self, start_time: str, end_time: str, slot: TimeSlot) -> bool:
        """Check if a time range fits within a time slot."""
        start_mins = self._time_to_minutes(start_time)
        end_mins = self._time_to_minutes(end_time)
        slot_start = self._time_to_minutes(slot.start_time)
        slot_end = self._time_to_minutes(slot.end_time)
        return start_mins >= slot_start and end_mins <= slot_end
    
    def _get_instances_per_week(self, frequency: Frequency) -> int:
        """Get the number of times per week an activity should occur."""
        frequency_map = {
            Frequency.DAILY: 7,
            Frequency.TWICE_DAILY: 14,
            Frequency.WEEKLY: 1,
            Frequency.TWICE_WEEKLY: 2,
            Frequency.THREE_TIMES_WEEKLY: 3,
            Frequency.MONTHLY: 0.25,  # Will be handled specially
            Frequency.AS_NEEDED: 0
        }
        return frequency_map.get(frequency, 1)
    
    def _get_preferred_time_range(self, slot_preference: str) -> Tuple[str, str]:
        """Get time range for a time slot preference."""
        time_ranges = {
            "morning": ("06:00", "12:00"),
            "afternoon": ("12:00", "17:00"),
            "evening": ("17:00", "22:00")
        }
        return time_ranges.get(slot_preference, ("06:00", "22:00"))
    
    def _find_available_slot(self, activity: Activity, date_str: str,
                             daily_schedule: Dict[str, List[Tuple[str, str]]]) -> Optional[Tuple[str, str]]:
        """
        Find an available time slot for an activity on a given date.
        
        Args:
            activity: The activity to schedule
            date_str: The date to schedule on
            daily_schedule: Already scheduled time slots for the day
            
        Returns:
            Tuple of (start_time, end_time) if found, None otherwise
        """
        # Get already booked slots for this date
        booked_slots = daily_schedule.get(date_str, [])
        
        # Try preferred time slots first
        for slot_pref in activity.preferred_time_slots or ["morning", "afternoon", "evening"]:
            range_start, range_end = self._get_preferred_time_range(slot_pref)
            slot = self._find_slot_in_range(activity, date_str, range_start, range_end, booked_slots)
            if slot:
                return slot
        
        # Try any available time
        return self._find_slot_in_range(activity, date_str, "06:00", "22:00", booked_slots)
    
    def _find_slot_in_range(self, activity: Activity, date_str: str,
                            range_start: str, range_end: str,
                            booked_slots: List[Tuple[str, str]]) -> Optional[Tuple[str, str]]:
        """Find an available slot within a time range."""
        duration = activity.duration_minutes
        current_time = self._time_to_minutes(range_start)
        end_time = self._time_to_minutes(range_end)
        
        while current_time + duration <= end_time:
            start_str = self._minutes_to_time(current_time)
            end_str = self._minutes_to_time(current_time + duration)
            
            # Check if this slot conflicts with booked slots
            conflict = False
            for booked_start, booked_end in booked_slots:
                if self._times_overlap(start_str, end_str, booked_start, booked_end):
                    conflict = True
                    # Move to after this booked slot
                    current_time = self._time_to_minutes(booked_end)
                    break
            
            if not conflict:
                # Check client availability
                if not self._is_client_available(date_str, start_str, end_str):
                    current_time += 30  # Try 30 minutes later
                    continue
                
                # Check equipment availability
                if not self._check_equipment_available(activity, date_str):
                    # If equipment not available and can't be done remotely, skip
                    if not activity.can_be_remote:
                        return None
                
                # Check specialist availability
                if not self._check_specialist_available(activity, date_str, start_str, end_str):
                    current_time += 30
                    continue
                
                # Check allied health availability
                if not self._check_allied_health_available(activity, date_str, start_str, end_str):
                    current_time += 30
                    continue
                
                return (start_str, end_str)
            
        return None
    
    def _handle_travel_day(self, activity: Activity, date_str: str) -> Optional[ScheduledActivity]:
        """
        Handle scheduling for days when client is traveling.
        
        During travel, only remote-capable activities can be scheduled.
        Some activities may be adapted (e.g., hotel gym instead of regular gym).
        
        Args:
            activity: The activity to potentially schedule
            date_str: The travel date
            
        Returns:
            ScheduledActivity if schedulable, None otherwise
        """
        travel = self.travel_by_date.get(date_str)
        
        # Medications should always be scheduled during travel
        if activity.activity_type == ActivityType.MEDICATION:
            return ScheduledActivity(
                activity=activity,
                scheduled_date=date_str,
                scheduled_time="08:00",
                end_time=self._minutes_to_time(
                    self._time_to_minutes("08:00") + activity.duration_minutes
                ),
                notes=f"During travel to {travel.destination}" if travel else "During travel"
            )
        
        # Remote-capable activities can be scheduled
        if activity.can_be_remote:
            return ScheduledActivity(
                activity=activity,
                scheduled_date=date_str,
                scheduled_time="09:00",
                end_time=self._minutes_to_time(
                    self._time_to_minutes("09:00") + activity.duration_minutes
                ),
                notes=f"Remote session during travel to {travel.destination}" if travel else "Remote session"
            )
        
        # Some fitness can be adapted during travel
        if activity.activity_type == ActivityType.FITNESS:
            if "Walk" in activity.name or "Stretch" in activity.name or "Yoga" in activity.name:
                return ScheduledActivity(
                    activity=activity,
                    scheduled_date=date_str,
                    scheduled_time="07:00",
                    end_time=self._minutes_to_time(
                        self._time_to_minutes("07:00") + activity.duration_minutes
                    ),
                    notes=f"Adapted for travel - can be done at hotel/destination"
                )
        
        return None
    
    def generate_schedule(self) -> List[ScheduledActivity]:
        """
        Generate the complete personalized schedule.
        
        This is the main scheduling method that:
        1. Iterates through each day in the date range
        2. Determines which activities need to be scheduled based on frequency
        3. Assigns time slots respecting all constraints
        4. Handles travel days and conflicts
        5. Falls back to backup activities when needed
        
        Returns:
            List of ScheduledActivity objects representing the full schedule
        """
        self.scheduled_activities = []
        daily_schedule: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        
        # Track weekly activity counts for frequency management
        weekly_counts: Dict[str, int] = defaultdict(int)
        monthly_counts: Dict[str, int] = defaultdict(int)
        
        current_date = self.start_date
        week_start = current_date
        month_start = current_date
        
        self.scheduling_log.append(f"Starting schedule generation from {self.start_date.strftime('%Y-%m-%d')} to {self.end_date.strftime('%Y-%m-%d')}")
        
        while current_date < self.end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            weekday = current_date.weekday()
            is_travel_day = date_str in self.travel_dates
            
            # Reset weekly counts at week start
            if (current_date - week_start).days >= 7:
                weekly_counts.clear()
                week_start = current_date
            
            # Reset monthly counts at month start
            if current_date.month != month_start.month:
                monthly_counts.clear()
                month_start = current_date
            
            self.scheduling_log.append(f"\n--- Scheduling for {date_str} ({['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][weekday]}) ---")
            if is_travel_day:
                travel = self.travel_by_date.get(date_str)
                self.scheduling_log.append(f"  Travel day: {travel.destination if travel else 'Unknown'}")
            
            # Schedule activities by priority
            for activity in self.activities:
                # Determine if this activity should be scheduled today
                should_schedule = self._should_schedule_today(
                    activity, current_date, weekly_counts, monthly_counts
                )
                
                if not should_schedule:
                    continue
                
                # Handle travel days specially
                if is_travel_day:
                    scheduled = self._handle_travel_day(activity, date_str)
                    if scheduled:
                        self.scheduled_activities.append(scheduled)
                        daily_schedule[date_str].append(
                            (scheduled.scheduled_time, scheduled.end_time)
                        )
                        weekly_counts[activity.id] += 1
                        monthly_counts[activity.id] += 1
                        self.scheduling_log.append(f"  ✓ Scheduled (travel): {activity.name} at {scheduled.scheduled_time}")
                    else:
                        self.scheduling_log.append(f"  ✗ Cannot schedule during travel: {activity.name}")
                    continue
                
                # Find available slot for regular days
                slot = self._find_available_slot(activity, date_str, daily_schedule)
                
                if slot:
                    start_time, end_time = slot
                    scheduled = ScheduledActivity(
                        activity=activity,
                        scheduled_date=date_str,
                        scheduled_time=start_time,
                        end_time=end_time
                    )
                    self.scheduled_activities.append(scheduled)
                    daily_schedule[date_str].append((start_time, end_time))
                    weekly_counts[activity.id] += 1
                    monthly_counts[activity.id] += 1
                    self.scheduling_log.append(f"  ✓ Scheduled: {activity.name} at {start_time}-{end_time}")
                else:
                    # Try backup activities
                    scheduled_backup = False
                    for backup_id in activity.backup_activities:
                        backup = next((a for a in self.activities if a.id == backup_id), None)
                        if backup:
                            backup_slot = self._find_available_slot(backup, date_str, daily_schedule)
                            if backup_slot:
                                start_time, end_time = backup_slot
                                scheduled = ScheduledActivity(
                                    activity=backup,
                                    scheduled_date=date_str,
                                    scheduled_time=start_time,
                                    end_time=end_time,
                                    is_backup=True,
                                    original_activity_id=activity.id,
                                    notes=f"Backup for {activity.name}"
                                )
                                self.scheduled_activities.append(scheduled)
                                daily_schedule[date_str].append((start_time, end_time))
                                weekly_counts[activity.id] += 1
                                monthly_counts[activity.id] += 1
                                self.scheduling_log.append(f"  ✓ Backup scheduled: {backup.name} for {activity.name}")
                                scheduled_backup = True
                                break
                    
                    if not scheduled_backup:
                        self.scheduling_log.append(f"  ✗ Could not schedule: {activity.name} - {activity.skip_adjustments}")
            
            current_date += timedelta(days=1)
        
        self.scheduling_log.append(f"\n=== Schedule generation complete: {len(self.scheduled_activities)} activities scheduled ===")
        return self.scheduled_activities
    
    def _should_schedule_today(self, activity: Activity, date: datetime,
                               weekly_counts: Dict[str, int],
                               monthly_counts: Dict[str, int]) -> bool:
        """
        Determine if an activity should be scheduled on a given day.
        
        Based on the activity's frequency and how many times it has
        already been scheduled this week/month.
        
        Args:
            activity: The activity to check
            date: The date to check
            weekly_counts: Count of this activity scheduled this week
            monthly_counts: Count of this activity scheduled this month
            
        Returns:
            True if the activity should be scheduled today
        """
        freq = activity.frequency
        current_count = weekly_counts.get(activity.id, 0)
        weekday = date.weekday()
        
        if freq == Frequency.DAILY:
            return True
        
        elif freq == Frequency.TWICE_DAILY:
            # Schedule twice per day - morning and evening
            return True
        
        elif freq == Frequency.WEEKLY:
            # Once per week - prefer Mondays or specific day
            if current_count >= 1:
                return False
            return weekday == 0 or weekday == 3  # Monday or Thursday
        
        elif freq == Frequency.TWICE_WEEKLY:
            if current_count >= 2:
                return False
            return weekday in [1, 4]  # Tuesday, Friday
        
        elif freq == Frequency.THREE_TIMES_WEEKLY:
            if current_count >= 3:
                return False
            return weekday in [0, 2, 4]  # Mon, Wed, Fri
        
        elif freq == Frequency.MONTHLY:
            monthly_count = monthly_counts.get(activity.id, 0)
            if monthly_count >= 1:
                return False
            return date.day == 15  # Mid-month
        
        elif freq == Frequency.AS_NEEDED:
            return False  # Don't auto-schedule
        
        return True
    
    def get_schedule_by_date(self) -> Dict[str, List[ScheduledActivity]]:
        """
        Get the schedule organized by date.
        
        Returns:
            Dictionary mapping dates to lists of scheduled activities
        """
        by_date = defaultdict(list)
        for scheduled in self.scheduled_activities:
            by_date[scheduled.scheduled_date].append(scheduled)
        
        # Sort each day's activities by time
        for date in by_date:
            by_date[date].sort(key=lambda x: x.scheduled_time)
        
        return dict(by_date)
    
    def get_schedule_by_week(self) -> Dict[str, Dict[str, List[ScheduledActivity]]]:
        """
        Get the schedule organized by week and day.
        
        Returns:
            Nested dictionary: week_number -> day -> activities
        """
        by_week = defaultdict(lambda: defaultdict(list))
        
        for scheduled in self.scheduled_activities:
            date = datetime.strptime(scheduled.scheduled_date, "%Y-%m-%d")
            week_num = date.isocalendar()[1]
            week_key = f"{date.year}-W{week_num:02d}"
            day_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][date.weekday()]
            by_week[week_key][day_name].append(scheduled)
        
        return dict(by_week)
    
    def get_statistics(self) -> Dict[str, any]:
        """
        Get scheduling statistics.
        
        Returns:
            Dictionary with scheduling statistics
        """
        by_type = defaultdict(int)
        by_priority = defaultdict(int)
        
        for scheduled in self.scheduled_activities:
            by_type[scheduled.activity.activity_type.value] += 1
            if scheduled.activity.priority <= 20:
                by_priority["critical"] += 1
            elif scheduled.activity.priority <= 50:
                by_priority["high"] += 1
            elif scheduled.activity.priority <= 80:
                by_priority["medium"] += 1
            else:
                by_priority["low"] += 1
        
        return {
            "total_scheduled": len(self.scheduled_activities),
            "by_type": dict(by_type),
            "by_priority": dict(by_priority),
            "backup_activities_used": sum(1 for s in self.scheduled_activities if s.is_backup),
            "date_range": {
                "start": self.start_date.strftime("%Y-%m-%d"),
                "end": self.end_date.strftime("%Y-%m-%d")
            }
        }


def load_data(data_dir: str = "data") -> Tuple:
    """
    Load all data from JSON files.
    
    Args:
        data_dir: Directory containing the data files
        
    Returns:
        Tuple of (activities, equipment, specialists, allied_health, travel_plans, client_schedule)
    """
    from models import Activity, Equipment, Specialist, AlliedHealth, TravelPlan, ClientSchedule, TimeSlot
    
    # Load activities
    with open(f"{data_dir}/activities.json", "r") as f:
        activities_data = json.load(f)
    activities = [Activity.from_dict(a) for a in activities_data]
    
    # Load equipment
    with open(f"{data_dir}/equipment.json", "r") as f:
        equipment_data = json.load(f)
    equipment = []
    for e in equipment_data:
        eq = Equipment(
            id=e["id"],
            name=e["name"],
            location=e["location"],
            availability_schedule=[TimeSlot(**slot) for slot in e["availability_schedule"]]
        )
        equipment.append(eq)
    
    # Load specialists
    with open(f"{data_dir}/specialists.json", "r") as f:
        specialists_data = json.load(f)
    specialists = []
    for s in specialists_data:
        spec = Specialist(
            id=s["id"],
            name=s["name"],
            specialty=s["specialty"],
            can_do_remote=s["can_do_remote"],
            availability_schedule=[TimeSlot(**slot) for slot in s["availability_schedule"]]
        )
        specialists.append(spec)
    
    # Load allied health
    with open(f"{data_dir}/allied_health.json", "r") as f:
        allied_health_data = json.load(f)
    allied_health = []
    for ah in allied_health_data:
        ah_obj = AlliedHealth(
            id=ah["id"],
            name=ah["name"],
            profession=ah["profession"],
            can_do_remote=ah["can_do_remote"],
            availability_schedule=[TimeSlot(**slot) for slot in ah["availability_schedule"]]
        )
        allied_health.append(ah_obj)
    
    # Load travel plans
    with open(f"{data_dir}/travel_plans.json", "r") as f:
        travel_plans_data = json.load(f)
    travel_plans = [TravelPlan(**tp) for tp in travel_plans_data]
    
    # Load client schedule
    with open(f"{data_dir}/client_schedule.json", "r") as f:
        client_schedule_data = json.load(f)
    client_schedule = ClientSchedule(
        blocked_times=[TimeSlot(**slot) for slot in client_schedule_data["blocked_times"]],
        preferred_workout_times=client_schedule_data["preferred_workout_times"],
        preferred_meal_times=client_schedule_data["preferred_meal_times"],
        wake_time=client_schedule_data["wake_time"],
        sleep_time=client_schedule_data["sleep_time"]
    )
    
    return activities, equipment, specialists, allied_health, travel_plans, client_schedule


if __name__ == "__main__":
    # Test the scheduler
    print("Loading data...")
    activities, equipment, specialists, allied_health, travel_plans, client_schedule = load_data("data")
    
    print(f"Loaded {len(activities)} activities")
    print(f"Loaded {len(equipment)} equipment items")
    print(f"Loaded {len(specialists)} specialists")
    print(f"Loaded {len(allied_health)} allied health professionals")
    
    # Create and run scheduler
    scheduler = ResourceAllocator(
        activities=activities,
        equipment=equipment,
        specialists=specialists,
        allied_health=allied_health,
        travel_plans=travel_plans,
        client_schedule=client_schedule,
        start_date="2026-01-15",
        end_date="2026-04-15"
    )
    
    print("\nGenerating schedule...")
    schedule = scheduler.generate_schedule()
    
    print("\n" + "=" * 50)
    stats = scheduler.get_statistics()
    print(f"Total activities scheduled: {stats['total_scheduled']}")
    print(f"By type: {stats['by_type']}")
    print(f"By priority: {stats['by_priority']}")
    print(f"Backup activities used: {stats['backup_activities_used']}")
