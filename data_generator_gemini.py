"""
data_generator_gemini.py - AI-Powered Test Data Generator using Gemini API

This module uses Google's Gemini AI to generate realistic health activities
and related data for the Resource Allocator system.

Set your Gemini API key in environment variable: GEMINI_API_KEY
Or create a .env file with: GEMINI_API_KEY=your_key_here
"""

import json
import csv
import random
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
try:
    import google.genai as genai
except ImportError:
    # Fallback to deprecated package
    import google.generativeai as genai
from models import (
    Activity, ActivityType, Frequency, TimeSlot,
    Equipment, Specialist, AlliedHealth, TravelPlan, ClientSchedule
)

# Load Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if not GEMINI_API_KEY:
    print(" Warning: GEMINI_API_KEY not set. Please set it in environment or .env file")
    print("   You can get a free API key from: https://makersuite.google.com/app/apikey")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class GeminiDataGenerator:
    """
    Generates realistic test data using Google's Gemini AI.
    
    This class uses AI to generate more diverse and realistic health activities
    compared to template-based generation.
    """
    
    def __init__(self, start_date: str = "2026-01-15", duration_months: int = 3):
        """
        Initialize the Gemini-powered data generator.
        
        Args:
            start_date: Start date for the schedule (YYYY-MM-DD format)
            duration_months: Number of months to generate schedules for
        """
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.duration_months = duration_months
        self.end_date = self.start_date + timedelta(days=duration_months * 30)
        self.model = None
        
        if GEMINI_API_KEY and genai:
            try:
                if GENAI_NEW:
                    # New package - try different initialization methods
                    try:
                        self.model = genai.GenerativeModel('gemini-pro', api_key=GEMINI_API_KEY)
                    except:
                        # Alternative initialization
                        genai.configure(api_key=GEMINI_API_KEY)
                        self.model = genai.GenerativeModel('gemini-pro')
                else:
                    # Old package
                    self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f" Error initializing Gemini: {e}")
                print("   Falling back to template-based generation")
                self.model = None
        else:
            self.model = None
            if not GEMINI_API_KEY:
                print("GEMINI_API_KEY not set. Using template-based generation.")
                print("   Get a free key from: https://makersuite.google.com/app/apikey")
    
    def _generate_with_gemini(self, prompt: str, max_retries: int = 3) -> Optional[str]:
        """
        Generate content using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            max_retries: Maximum number of retry attempts
            
        Returns:
            Generated text or None if failed
        """
        if not self.model:
            return None
        
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                # Handle both new and old package response formats
                if hasattr(response, 'text'):
                    return response.text
                elif hasattr(response, 'candidates') and response.candidates:
                    return response.candidates[0].content.parts[0].text
                else:
                    return str(response)
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"   Retry {attempt + 1}/{max_retries}...")
                    continue
                else:
                    print(f"   Error: {e}")
                    return None
        return None
    
    def _parse_json_from_response(self, response: str) -> Optional[Dict]:
        """Parse JSON from Gemini response, handling markdown code blocks."""
        try:
            # Remove markdown code blocks if present
            if '```json' in response:
                response = response.split('```json')[1].split('```')[0]
            elif '```' in response:
                response = response.split('```')[1].split('```')[0]
            
            return json.loads(response.strip())
        except Exception as e:
            print(f"   Error parsing JSON: {e}")
            return None
    
    def generate_activities_with_gemini(self) -> List[Activity]:
        """
        Generate health activities using Gemini AI.
        
        Returns:
            List of Activity objects
        """
        if not self.model:
            print("⚠️  Gemini API not available, using fallback templates")
            return self._generate_fallback_activities()
        
        print("🤖 Generating activities with Gemini AI...")
        activities = []
        activity_id = 1
        
        # Generate activities by category
        categories = [
            ("fitness", 20, "Generate 20 diverse fitness activities including cardio, strength training, flexibility, and specialized exercises. Include activities like running, weightlifting, yoga, swimming, cycling, and unique fitness routines."),
            ("food", 15, "Generate 15 nutrition and meal-related activities including meals, supplements, hydration, and dietary practices. Include breakfast, lunch, dinner, supplements, and special nutrition protocols."),
            ("medication", 8, "Generate 8 medication activities with specific timing requirements. Include medications for blood pressure, thyroid, diabetes, cholesterol, and other common health conditions."),
            ("therapy", 12, "Generate 12 therapy and wellness activities including sauna, cold therapy, massage, acupuncture, and other recovery/therapeutic modalities."),
            ("consultation", 14, "Generate 14 consultation activities with various healthcare professionals including cardiologists, nutritionists, physical therapists, and other specialists.")
        ]
        
        for activity_type_str, count, description in categories:
            print(f"   Generating {count} {activity_type_str} activities...")
            
            prompt = f"""
Generate {count} realistic health activities for a personalized health schedule system.

Category: {activity_type_str}
Description: {description}

For each activity, provide:
- name: A descriptive name
- details: Specific instructions or parameters (e.g., "Maintain HR between 120-140 BPM")
- duration: Duration in minutes (5-120)
- facilitator: Who facilitates (e.g., "Personal Trainer", "Self", "Doctor")
- location: Where it happens (e.g., "Gym", "Home", "Clinic")
- equipment: List of equipment IDs needed (use realistic IDs like "heart_rate_monitor", "dumbbells", etc.)
- metrics: List of metrics to collect (e.g., ["heart_rate", "distance", "calories"])
- can_be_remote: true/false
- prep_requirements: Preparation needed
- frequency_suggestion: Suggested frequency (daily, weekly, twice_weekly, etc.)
- priority_range: Priority range (1-100, lower is more important)

Return ONLY a JSON array with this structure:
[
  {{
    "name": "Activity Name",
    "details": "Specific details",
    "duration": 45,
    "facilitator": "Facilitator Name",
    "location": "Location",
    "equipment": ["equipment_id1", "equipment_id2"],
    "metrics": ["metric1", "metric2"],
    "can_be_remote": false,
    "prep_requirements": "Prep needed",
    "frequency_suggestion": "weekly",
    "priority_range": "21-50"
  }}
]

Make activities diverse, realistic, and suitable for a health optimization program.
"""
            
            response = self._generate_with_gemini(prompt)
            if not response:
                print(f"   ⚠️  Failed to generate {activity_type_str} activities, using fallback")
                activities.extend(self._generate_fallback_by_type(activity_type_str, count, activity_id))
                activity_id += count
                continue
            
            # Parse response
            parsed = self._parse_json_from_response(response)
            if not parsed or not isinstance(parsed, list):
                print(f"   ⚠️  Invalid response for {activity_type_str}, using fallback")
                activities.extend(self._generate_fallback_by_type(activity_type_str, count, activity_id))
                activity_id += count
                continue
            
            # Convert to Activity objects
            activity_type = ActivityType(activity_type_str)
            for item in parsed[:count]:  # Limit to requested count
                try:
                    # Parse priority range
                    priority_range = item.get('priority_range', '21-50')
                    if '-' in priority_range:
                        low, high = map(int, priority_range.split('-'))
                        priority = random.randint(low, high)
                    else:
                        priority = int(priority_range)
                    
                    # Map frequency
                    freq_str = item.get('frequency_suggestion', 'weekly').lower()
                    frequency_map = {
                        'daily': Frequency.DAILY,
                        'twice_daily': Frequency.TWICE_DAILY,
                        'weekly': Frequency.WEEKLY,
                        'twice_weekly': Frequency.TWICE_WEEKLY,
                        'three_times_weekly': Frequency.THREE_TIMES_WEEKLY,
                        'monthly': Frequency.MONTHLY,
                        'as_needed': Frequency.AS_NEEDED
                    }
                    frequency = frequency_map.get(freq_str, Frequency.WEEKLY)
                    
                    activity = Activity(
                        id=f"ACT_{activity_id:03d}",
                        name=item.get('name', f'{activity_type_str.title()} Activity'),
                        activity_type=activity_type,
                        priority=priority,
                        frequency=frequency,
                        duration_minutes=item.get('duration', 30),
                        details=item.get('details', ''),
                        facilitator=item.get('facilitator', 'Self'),
                        location=item.get('location', 'Home'),
                        can_be_remote=item.get('can_be_remote', False),
                        prep_requirements=item.get('prep_requirements', ''),
                        backup_activities=[],
                        skip_adjustments="Reschedule if missed",
                        metrics_to_collect=item.get('metrics', []),
                        equipment_needed=item.get('equipment', []),
                        preferred_time_slots=self._get_preferred_slots_for_type(activity_type_str)
                    )
                    activities.append(activity)
                    activity_id += 1
                except Exception as e:
                    print(f"   ⚠️  Error creating activity: {e}")
                    continue
        
        print(f"✅ Generated {len(activities)} activities with Gemini AI")
        return activities
    
    def _get_preferred_slots_for_type(self, activity_type: str) -> List[str]:
        """Get preferred time slots based on activity type."""
        if activity_type == "medication":
            return ["morning", "evening"]
        elif activity_type == "food":
            return ["morning", "afternoon", "evening"]
        elif activity_type == "fitness":
            return ["morning", "evening"]
        else:
            return ["morning", "afternoon", "evening"]
    
    def _generate_fallback_activities(self) -> List[Activity]:
        """Fallback to template-based generation if Gemini fails."""
        from data_generator import DataGenerator
        fallback_gen = DataGenerator(
            start_date=self.start_date.strftime("%Y-%m-%d"),
            duration_months=self.duration_months
        )
        return fallback_gen.generate_activities()
    
    def _generate_fallback_by_type(self, activity_type: str, count: int, start_id: int) -> List[Activity]:
        """Generate fallback activities for a specific type."""
        activities = []
        activity_type_enum = ActivityType(activity_type)
        
        for i in range(count):
            activity = Activity(
                id=f"ACT_{start_id + i:03d}",
                name=f"{activity_type.title()} Activity {i+1}",
                activity_type=activity_type_enum,
                priority=random.randint(1, 100),
                frequency=random.choice(list(Frequency)),
                duration_minutes=random.randint(10, 60),
                details=f"AI-generated {activity_type} activity",
                facilitator="Self",
                location="Home",
                can_be_remote=random.choice([True, False]),
                prep_requirements="",
                backup_activities=[],
                skip_adjustments="Reschedule if missed",
                metrics_to_collect=["completion"],
                equipment_needed=[],
                preferred_time_slots=self._get_preferred_slots_for_type(activity_type)
            )
            activities.append(activity)
        
        return activities
    
    def generate_equipment_availability(self) -> List[Equipment]:
        """Generate equipment with availability schedules (same as original)."""
        # Equipment list (can also be AI-generated, but keeping simple for now)
        equipment_data = [
            {"id": "heart_rate_monitor", "name": "Heart Rate Monitor", "location": "Personal"},
            {"id": "running_watch", "name": "Running GPS Watch", "location": "Personal"},
            {"id": "treadmill", "name": "Treadmill", "location": "Gym"},
            {"id": "barbell", "name": "Olympic Barbell", "location": "Gym"},
            {"id": "dumbbells", "name": "Dumbbell Set", "location": "Gym"},
            {"id": "yoga_mat", "name": "Yoga Mat", "location": "Personal"},
            {"id": "bicycle", "name": "Road Bicycle", "location": "Home"},
            {"id": "infrared_sauna", "name": "Infrared Sauna", "location": "Wellness Center"},
            {"id": "cold_plunge_tub", "name": "Cold Plunge Tub", "location": "Wellness Center"},
        ]
        
        equipment_list = []
        for eq_data in equipment_data:
            availability = []
            current_date = self.start_date
            
            while current_date < self.end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                weekday = current_date.weekday()
                
                if eq_data["location"] == "Personal" or eq_data["location"] == "Home":
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="06:00",
                        end_time="22:00",
                        is_available=True
                    ))
                elif eq_data["location"] == "Gym":
                    is_available = weekday != 6  # Closed Sunday
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="06:00",
                        end_time="22:00",
                        is_available=is_available
                    ))
                else:
                    is_available = weekday < 6  # Mon-Sat
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="09:00",
                        end_time="20:00",
                        is_available=is_available
                    ))
                
                current_date += timedelta(days=1)
            
            equipment = Equipment(
                id=eq_data["id"],
                name=eq_data["name"],
                location=eq_data["location"],
                availability_schedule=availability
            )
            equipment_list.append(equipment)
        
        return equipment_list
    
    def generate_specialist_availability(self) -> List[Specialist]:
        """Generate specialists with schedules (same as original)."""
        specialists_data = [
            {"id": "cardiologist", "name": "Dr. Sarah Chen", "specialty": "Cardiology", "remote": True},
            {"id": "endocrinologist", "name": "Dr. Michael Ross", "specialty": "Endocrinology", "remote": True},
            {"id": "psychiatrist", "name": "Dr. Emily Watson", "specialty": "Psychiatry", "remote": True},
            {"id": "dermatologist", "name": "Dr. James Park", "specialty": "Dermatology", "remote": False},
        ]
        
        specialists = []
        for spec_data in specialists_data:
            availability = []
            current_date = self.start_date
            working_days = random.sample([0, 1, 2, 3, 4], k=random.randint(3, 5))
            
            while current_date < self.end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                weekday = current_date.weekday()
                is_working_day = weekday in working_days
                is_available = is_working_day and random.random() > 0.05
                
                if is_available:
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="09:00",
                        end_time="12:00",
                        is_available=True
                    ))
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="14:00",
                        end_time="17:00",
                        is_available=True
                    ))
                
                current_date += timedelta(days=1)
            
            specialist = Specialist(
                id=spec_data["id"],
                name=spec_data["name"],
                specialty=spec_data["specialty"],
                can_do_remote=spec_data["remote"],
                availability_schedule=availability
            )
            specialists.append(specialist)
        
        return specialists
    
    def generate_allied_health_availability(self) -> List[AlliedHealth]:
        """Generate allied health professionals (same as original)."""
        allied_health_data = [
            {"id": "physiotherapist", "name": "Tom Richards", "profession": "Physiotherapist", "remote": False},
            {"id": "dietitian", "name": "Sarah Johnson", "profession": "Registered Dietitian", "remote": True},
            {"id": "health_coach", "name": "Rachel Green", "profession": "Certified Health Coach", "remote": True},
        ]
        
        allied_health = []
        for ah_data in allied_health_data:
            availability = []
            current_date = self.start_date
            working_days = random.sample([0, 1, 2, 3, 4, 5], k=random.randint(4, 5))
            
            while current_date < self.end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                weekday = current_date.weekday()
                is_working_day = weekday in working_days
                is_available = is_working_day and random.random() > 0.03
                
                if is_available:
                    for start_hour, end_hour in [(8, 12), (13, 17)]:
                        availability.append(TimeSlot(
                            date=date_str,
                            start_time=f"{start_hour:02d}:00",
                            end_time=f"{end_hour:02d}:00",
                            is_available=True
                        ))
                
                current_date += timedelta(days=1)
            
            ah = AlliedHealth(
                id=ah_data["id"],
                name=ah_data["name"],
                profession=ah_data["profession"],
                can_do_remote=ah_data["remote"],
                availability_schedule=availability
            )
            allied_health.append(ah)
        
        return allied_health
    
    def generate_travel_plans(self) -> List[TravelPlan]:
        """Generate travel plans (same as original)."""
        return [
            TravelPlan(
                id="TRAVEL_001",
                destination="New York City",
                start_date=(self.start_date + timedelta(days=15)).strftime("%Y-%m-%d"),
                end_date=(self.start_date + timedelta(days=18)).strftime("%Y-%m-%d"),
                timezone="America/New_York",
                notes="Business conference"
            ),
            TravelPlan(
                id="TRAVEL_002",
                destination="Hawaii",
                start_date=(self.start_date + timedelta(days=45)).strftime("%Y-%m-%d"),
                end_date=(self.start_date + timedelta(days=52)).strftime("%Y-%m-%d"),
                timezone="Pacific/Honolulu",
                notes="Family vacation"
            ),
        ]
    
    def generate_client_schedule(self) -> ClientSchedule:
        """Generate client schedule (same as original)."""
        blocked_times = []
        current_date = self.start_date
        
        while current_date < self.end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            weekday = current_date.weekday()
            
            if weekday < 5:  # Mon-Fri
                blocked_times.append(TimeSlot(
                    date=date_str,
                    start_time="09:00",
                    end_time="17:00",
                    is_available=False,
                    notes="Work hours"
                ))
            
            current_date += timedelta(days=1)
        
        return ClientSchedule(
            blocked_times=blocked_times,
            preferred_workout_times=["morning", "evening"],
            preferred_meal_times={
                "breakfast": "07:30",
                "lunch": "12:30",
                "dinner": "19:00"
            },
            wake_time="06:00",
            sleep_time="22:30"
        )
    
    def save_all_data(self, output_dir: str = "data"):
        """
        Generate and save all test data using Gemini AI.
        
        Args:
            output_dir: Directory to save the data files
        """
        print("\n" + "=" * 60)
        print("🤖 GENERATING DATA WITH GEMINI AI")
        print("=" * 60)
        
        # Generate activities with Gemini
        activities = self.generate_activities_with_gemini()
        
        # Generate other data (equipment, specialists, etc.)
        print("\nGenerating equipment availability...")
        equipment = self.generate_equipment_availability()
        
        print("Generating specialist availability...")
        specialists = self.generate_specialist_availability()
        
        print("Generating allied health availability...")
        allied_health = self.generate_allied_health_availability()
        
        print("Generating travel plans...")
        travel_plans = self.generate_travel_plans()
        
        print("Generating client schedule...")
        client_schedule = self.generate_client_schedule()
        
        # Save to files
        os.makedirs(output_dir, exist_ok=True)
        
        # Save activities
        activities_data = [a.to_dict() for a in activities]
        with open(f"{output_dir}/activities.json", "w") as f:
            json.dump(activities_data, f, indent=2)
        
        # Save CSV
        self._save_activities_csv(activities, f"{output_dir}/activities.csv")
        
        # Save other data
        equipment_data = [e.to_dict() for e in equipment]
        with open(f"{output_dir}/equipment.json", "w") as f:
            json.dump(equipment_data, f, indent=2)
        
        specialists_data = [s.to_dict() for s in specialists]
        with open(f"{output_dir}/specialists.json", "w") as f:
            json.dump(specialists_data, f, indent=2)
        
        allied_health_data = [ah.to_dict() for ah in allied_health]
        with open(f"{output_dir}/allied_health.json", "w") as f:
            json.dump(allied_health_data, f, indent=2)
        
        travel_plans_data = [tp.to_dict() for tp in travel_plans]
        with open(f"{output_dir}/travel_plans.json", "w") as f:
            json.dump(travel_plans_data, f, indent=2)
        
        with open(f"{output_dir}/client_schedule.json", "w") as f:
            json.dump(client_schedule.to_dict(), f, indent=2)
        
        print("\n" + "=" * 60)
        print(f"✅ Generated {len(activities)} activities with Gemini AI")
        print(f"✅ Generated {len(equipment)} equipment items")
        print(f"✅ Generated {len(specialists)} specialists")
        print(f"✅ Generated {len(allied_health)} allied health professionals")
        print(f"✅ Generated {len(travel_plans)} travel plans")
        print(f"✅ All data saved to {output_dir}/")
        print("=" * 60)
        
        return {
            "activities": activities,
            "equipment": equipment,
            "specialists": specialists,
            "allied_health": allied_health,
            "travel_plans": travel_plans,
            "client_schedule": client_schedule
        }
    
    def _save_activities_csv(self, activities: List[Activity], filepath: str):
        """Save activities to CSV format."""
        fieldnames = [
            "id", "name", "activity_type", "priority", "frequency",
            "duration_minutes", "details", "facilitator", "location",
            "can_be_remote", "prep_requirements", "backup_activities",
            "skip_adjustments", "metrics_to_collect", "equipment_needed",
            "specialist_needed", "allied_health_needed", "preferred_time_slots"
        ]
        
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for activity in activities:
                row = activity.to_dict()
                row["backup_activities"] = "|".join(row["backup_activities"])
                row["metrics_to_collect"] = "|".join(row["metrics_to_collect"])
                row["equipment_needed"] = "|".join(row["equipment_needed"])
                row["preferred_time_slots"] = "|".join(row["preferred_time_slots"])
                writer.writerow(row)


if __name__ == "__main__":
    # Check for API key
    if not GEMINI_API_KEY:
        print("=" * 60)
        print(" GEMINI_API_KEY not found!")
        print("=" * 60)
        print("To use Gemini AI for data generation:")
        print("1. Get a free API key from: https://makersuite.google.com/app/apikey")
        print("2. Set it as environment variable:")
        print("   export GEMINI_API_KEY='your_key_here'")
        print("3. Or create a .env file with: GEMINI_API_KEY=your_key_here")
        print("=" * 60)
        print("\nFalling back to template-based generation...")
        from data_generator import DataGenerator
        generator = DataGenerator(start_date="2026-01-15", duration_months=3)
        generator.save_all_data("data")
    else:
        # Use Gemini-powered generator
        generator = GeminiDataGenerator(start_date="2026-01-15", duration_months=3)
        generator.save_all_data("data")
