"""
models.py - Data Models for the Resource Allocator System

This module defines all the data structures used in the Resource Allocator.
It uses Python dataclasses for clean, type-annotated data structures.

The Resource Allocator coordinates:
- Action Plans (activities to be scheduled)
- Resources (equipment, specialists, allied health professionals)
- Constraints (travel plans, client schedules)
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime, time


class ActivityType(Enum):
    """
    Enum representing the different types of activities that can be scheduled.
    
    FITNESS: Exercise routines including eye exercises, cardio, strength training
    FOOD: Meal consumption, supplement intake, dietary requirements
    MEDICATION: Prescription medications, supplements, vitamins
    THERAPY: Therapeutic activities like sauna, ice bath, massage
    CONSULTATION: Meetings with healthcare professionals
    """
    FITNESS = "fitness"
    FOOD = "food"
    MEDICATION = "medication"
    THERAPY = "therapy"
    CONSULTATION = "consultation"


class Frequency(Enum):
    """
    Enum representing how often an activity needs to be performed.
    """
    DAILY = "daily"
    TWICE_DAILY = "twice_daily"
    WEEKLY = "weekly"
    TWICE_WEEKLY = "twice_weekly"
    THREE_TIMES_WEEKLY = "three_times_weekly"
    MONTHLY = "monthly"
    AS_NEEDED = "as_needed"


@dataclass
class Activity:
    """
    Represents a single activity in the action plan.
    
    Attributes:
        id: Unique identifier for the activity
        name: Human-readable name of the activity
        activity_type: Category of activity (fitness, food, medication, etc.)
        priority: Priority level (1 = highest priority, based on health importance)
        frequency: How often the activity needs to be performed
        duration_minutes: Expected duration of the activity
        details: Specific instructions or parameters (e.g., "HR between 120-140")
        facilitator: Who facilitates this activity (e.g., "trainer", "nutritionist")
        location: Where the activity can be performed
        can_be_remote: Whether the activity can be done via video call
        prep_requirements: Any preparation needed before the activity
        backup_activities: List of alternative activity IDs that can substitute
        skip_adjustments: What to do if the activity is skipped
        metrics_to_collect: Data to be recorded from this activity
        equipment_needed: List of equipment IDs required
        specialist_needed: Specialist ID if a specialist is required
        allied_health_needed: Allied health professional ID if needed
        preferred_time_slots: Preferred times of day for this activity
    """
    id: str
    name: str
    activity_type: ActivityType
    priority: int
    frequency: Frequency
    duration_minutes: int
    details: str = ""
    facilitator: str = ""
    location: str = ""
    can_be_remote: bool = False
    prep_requirements: str = ""
    backup_activities: List[str] = field(default_factory=list)
    skip_adjustments: str = ""
    metrics_to_collect: List[str] = field(default_factory=list)
    equipment_needed: List[str] = field(default_factory=list)
    specialist_needed: Optional[str] = None
    allied_health_needed: Optional[str] = None
    preferred_time_slots: List[str] = field(default_factory=list)  # "morning", "afternoon", "evening"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert activity to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "activity_type": self.activity_type.value,
            "priority": self.priority,
            "frequency": self.frequency.value,
            "duration_minutes": self.duration_minutes,
            "details": self.details,
            "facilitator": self.facilitator,
            "location": self.location,
            "can_be_remote": self.can_be_remote,
            "prep_requirements": self.prep_requirements,
            "backup_activities": self.backup_activities,
            "skip_adjustments": self.skip_adjustments,
            "metrics_to_collect": self.metrics_to_collect,
            "equipment_needed": self.equipment_needed,
            "specialist_needed": self.specialist_needed,
            "allied_health_needed": self.allied_health_needed,
            "preferred_time_slots": self.preferred_time_slots
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Activity':
        """Create an Activity from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            activity_type=ActivityType(data["activity_type"]),
            priority=data["priority"],
            frequency=Frequency(data["frequency"]),
            duration_minutes=data["duration_minutes"],
            details=data.get("details", ""),
            facilitator=data.get("facilitator", ""),
            location=data.get("location", ""),
            can_be_remote=data.get("can_be_remote", False),
            prep_requirements=data.get("prep_requirements", ""),
            backup_activities=data.get("backup_activities", []),
            skip_adjustments=data.get("skip_adjustments", ""),
            metrics_to_collect=data.get("metrics_to_collect", []),
            equipment_needed=data.get("equipment_needed", []),
            specialist_needed=data.get("specialist_needed"),
            allied_health_needed=data.get("allied_health_needed"),
            preferred_time_slots=data.get("preferred_time_slots", [])
        )


@dataclass
class TimeSlot:
    """
    Represents an available time slot.
    
    Attributes:
        date: The date of the time slot
        start_time: Start time of availability
        end_time: End time of availability
        is_available: Whether this slot is available
        notes: Any additional notes about the slot
    """
    date: str  # YYYY-MM-DD format
    start_time: str  # HH:MM format
    end_time: str  # HH:MM format
    is_available: bool = True
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "date": self.date,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "is_available": self.is_available,
            "notes": self.notes
        }


@dataclass
class Equipment:
    """
    Represents equipment that may be needed for activities.
    
    Attributes:
        id: Unique identifier
        name: Equipment name
        location: Where the equipment is located
        availability_schedule: List of available time slots
    """
    id: str
    name: str
    location: str
    availability_schedule: List[TimeSlot] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "availability_schedule": [slot.to_dict() for slot in self.availability_schedule]
        }


@dataclass
class Specialist:
    """
    Represents a medical specialist.
    
    Attributes:
        id: Unique identifier
        name: Specialist's name
        specialty: Area of expertise
        can_do_remote: Whether they offer remote consultations
        availability_schedule: List of available time slots
    """
    id: str
    name: str
    specialty: str
    can_do_remote: bool = True
    availability_schedule: List[TimeSlot] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "can_do_remote": self.can_do_remote,
            "availability_schedule": [slot.to_dict() for slot in self.availability_schedule]
        }


@dataclass
class AlliedHealth:
    """
    Represents an allied health professional (non-doctor healthcare provider).
    
    Examples: Physiotherapists, dietitians, occupational therapists, etc.
    
    Attributes:
        id: Unique identifier
        name: Professional's name
        profession: Type of allied health professional
        can_do_remote: Whether they offer remote sessions
        availability_schedule: List of available time slots
    """
    id: str
    name: str
    profession: str
    can_do_remote: bool = True
    availability_schedule: List[TimeSlot] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "profession": self.profession,
            "can_do_remote": self.can_do_remote,
            "availability_schedule": [slot.to_dict() for slot in self.availability_schedule]
        }


@dataclass
class TravelPlan:
    """
    Represents a travel commitment that affects availability.
    
    Attributes:
        id: Unique identifier
        destination: Where the client is traveling to
        start_date: Travel start date (YYYY-MM-DD)
        end_date: Travel end date (YYYY-MM-DD)
        timezone: Timezone of the destination
        notes: Any relevant notes about the travel
    """
    id: str
    destination: str
    start_date: str
    end_date: str
    timezone: str = "UTC"
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "destination": self.destination,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "timezone": self.timezone,
            "notes": self.notes
        }


@dataclass
class ClientSchedule:
    """
    Represents the client's personal schedule constraints.
    
    Attributes:
        blocked_times: List of time slots when client is unavailable
        preferred_workout_times: Preferred times for exercise
        preferred_meal_times: Regular meal times
        wake_time: Typical wake up time
        sleep_time: Typical bedtime
    """
    blocked_times: List[TimeSlot] = field(default_factory=list)
    preferred_workout_times: List[str] = field(default_factory=list)  # ["morning", "evening"]
    preferred_meal_times: Dict[str, str] = field(default_factory=dict)  # {"breakfast": "08:00", ...}
    wake_time: str = "06:00"
    sleep_time: str = "22:00"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "blocked_times": [slot.to_dict() for slot in self.blocked_times],
            "preferred_workout_times": self.preferred_workout_times,
            "preferred_meal_times": self.preferred_meal_times,
            "wake_time": self.wake_time,
            "sleep_time": self.sleep_time
        }


@dataclass
class ScheduledActivity:
    """
    Represents a scheduled instance of an activity in the personalized plan.
    
    Attributes:
        activity: The original activity being scheduled
        scheduled_date: Date when the activity is scheduled
        scheduled_time: Time when the activity starts
        end_time: Time when the activity ends
        is_backup: Whether this is a backup activity substitution
        original_activity_id: If backup, the ID of the original activity
        notes: Any scheduling notes
    """
    activity: Activity
    scheduled_date: str
    scheduled_time: str
    end_time: str
    is_backup: bool = False
    original_activity_id: Optional[str] = None
    notes: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "activity_id": self.activity.id,
            "activity_name": self.activity.name,
            "activity_type": self.activity.activity_type.value,
            "scheduled_date": self.scheduled_date,
            "scheduled_time": self.scheduled_time,
            "end_time": self.end_time,
            "duration_minutes": self.activity.duration_minutes,
            "details": self.activity.details,
            "facilitator": self.activity.facilitator,
            "location": self.activity.location,
            "is_remote": self.activity.can_be_remote,
            "is_backup": self.is_backup,
            "original_activity_id": self.original_activity_id,
            "notes": self.notes
        }
