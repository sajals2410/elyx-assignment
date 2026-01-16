"""
data_generator.py - Realistic Test Data Generator for Resource Allocator

This module generates realistic sample data including:
- 100+ health-related activities with proper priorities and details
- Equipment availability schedules for 3 months
- Specialist availability schedules for 3 months
- Allied health professional schedules for 3 months
- Client schedule constraints
- Travel plans

The data is designed to simulate a real-world health optimization scenario
for a client following Elyx's HealthSpan AI recommendations.
"""

import json
import csv
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any
from models import (
    Activity, ActivityType, Frequency, TimeSlot,
    Equipment, Specialist, AlliedHealth, TravelPlan, ClientSchedule
)


# ============================================================================
# CONFIGURATION: Realistic data templates for generation
# ============================================================================

# Fitness activities with realistic details
FITNESS_ACTIVITIES = [
    {"name": "Morning Zone 2 Cardio Run", "details": "Maintain HR between 120-140 BPM, nasal breathing", "duration": 45, "facilitator": "Running Coach", "location": "Outdoor Track", "equipment": ["heart_rate_monitor", "running_watch"], "metrics": ["heart_rate", "distance", "pace", "cadence"]},
    {"name": "High-Intensity Interval Training", "details": "4x4 protocol: 4 min high intensity, 3 min recovery", "duration": 30, "facilitator": "Personal Trainer", "location": "Gym", "equipment": ["treadmill", "heart_rate_monitor"], "metrics": ["heart_rate_max", "calories_burned", "vo2_estimate"]},
    {"name": "Strength Training - Upper Body", "details": "Focus on compound movements: bench press, rows, shoulder press", "duration": 60, "facilitator": "Strength Coach", "location": "Gym", "equipment": ["barbell", "dumbbells", "bench"], "metrics": ["weight_lifted", "reps", "sets", "rpe"]},
    {"name": "Strength Training - Lower Body", "details": "Squats, deadlifts, lunges - progressive overload protocol", "duration": 60, "facilitator": "Strength Coach", "location": "Gym", "equipment": ["barbell", "squat_rack", "leg_press"], "metrics": ["weight_lifted", "reps", "sets", "rpe"]},
    {"name": "Yoga Flow Session", "details": "Vinyasa flow focusing on flexibility and breath work", "duration": 45, "facilitator": "Yoga Instructor", "location": "Yoga Studio", "equipment": ["yoga_mat"], "metrics": ["flexibility_score", "breath_count"]},
    {"name": "Swimming Laps", "details": "Mixed strokes, focus on endurance and technique", "duration": 40, "facilitator": "Swim Coach", "location": "Pool", "equipment": ["swim_goggles", "swim_cap"], "metrics": ["laps_completed", "stroke_count", "time_per_lap"]},
    {"name": "Cycling Session", "details": "Zone 2 endurance ride, flat terrain", "duration": 60, "facilitator": "Cycling Coach", "location": "Indoor/Outdoor", "equipment": ["bicycle", "cycling_computer"], "metrics": ["distance", "average_speed", "cadence", "heart_rate"]},
    {"name": "Eye Exercise Routine", "details": "Bates method exercises for eye health - 20-20-20 rule compliance", "duration": 10, "facilitator": "Self", "location": "Home", "equipment": [], "metrics": ["completion", "eye_strain_level"], "remote": True},
    {"name": "Core Stability Workout", "details": "Planks, dead bugs, bird dogs - focus on anti-rotation", "duration": 20, "facilitator": "Personal Trainer", "location": "Gym", "equipment": ["exercise_mat"], "metrics": ["hold_times", "reps"]},
    {"name": "Mobility and Stretching", "details": "Dynamic and static stretching routine", "duration": 15, "facilitator": "Self", "location": "Home", "equipment": ["foam_roller", "exercise_mat"], "metrics": ["flexibility_assessment"]},
    {"name": "Walking Meditation", "details": "Mindful walking at slow pace, focus on breathing", "duration": 30, "facilitator": "Self", "location": "Park", "equipment": [], "metrics": ["steps", "mindfulness_rating"]},
    {"name": "Resistance Band Training", "details": "Full body resistance training with bands", "duration": 30, "facilitator": "Physical Therapist", "location": "Home", "equipment": ["resistance_bands"], "metrics": ["reps", "resistance_level"]},
    {"name": "Balance Training", "details": "Single leg stands, BOSU ball exercises", "duration": 20, "facilitator": "Personal Trainer", "location": "Gym", "equipment": ["bosu_ball", "balance_board"], "metrics": ["balance_time", "falls"]},
    {"name": "Rowing Machine Workout", "details": "500m intervals with active recovery", "duration": 25, "facilitator": "Rowing Coach", "location": "Gym", "equipment": ["rowing_machine"], "metrics": ["split_time", "stroke_rate", "distance"]},
    {"name": "Pilates Session", "details": "Mat Pilates focusing on core and posture", "duration": 45, "facilitator": "Pilates Instructor", "location": "Studio", "equipment": ["pilates_mat", "pilates_ring"], "metrics": ["form_score", "exercises_completed"]},
    {"name": "Stair Climbing", "details": "Building stairs for cardio, 10 floors minimum", "duration": 15, "facilitator": "Self", "location": "Building", "equipment": [], "metrics": ["floors_climbed", "heart_rate"]},
    {"name": "Kettlebell Training", "details": "Swings, Turkish get-ups, goblet squats", "duration": 30, "facilitator": "Kettlebell Instructor", "location": "Gym", "equipment": ["kettlebells"], "metrics": ["weight", "reps", "form_rating"]},
    {"name": "Tai Chi Practice", "details": "Slow form practice for balance and mindfulness", "duration": 30, "facilitator": "Tai Chi Instructor", "location": "Park", "equipment": [], "metrics": ["form_completion", "balance_rating"]},
    {"name": "Boxing/Kickboxing", "details": "Pad work and bag work for cardio and coordination", "duration": 45, "facilitator": "Boxing Coach", "location": "Boxing Gym", "equipment": ["boxing_gloves", "heavy_bag"], "metrics": ["punches_thrown", "calories_burned"]},
    {"name": "Functional Movement Screen", "details": "Assessment of movement patterns and mobility", "duration": 30, "facilitator": "Physical Therapist", "location": "Clinic", "equipment": ["fms_kit"], "metrics": ["fms_score", "asymmetries_noted"]},
]

# Food/Nutrition activities
FOOD_ACTIVITIES = [
    {"name": "Protein-Rich Breakfast", "details": "30g protein minimum, low glycemic carbs", "duration": 20, "facilitator": "Self", "location": "Home", "prep": "Meal prep required night before", "metrics": ["protein_grams", "calories", "glycemic_load"]},
    {"name": "Mid-Morning Supplement Stack", "details": "Vitamin D3, Omega-3, Magnesium glycinate", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Organize pill box weekly", "metrics": ["supplements_taken", "time_taken"]},
    {"name": "Pre-Workout Nutrition", "details": "Light carbs and caffeine 45 min before exercise", "duration": 10, "facilitator": "Self", "location": "Home", "prep": "Prepare smoothie ingredients", "metrics": ["timing_accuracy", "energy_level"]},
    {"name": "Post-Workout Recovery Shake", "details": "Whey protein, creatine, fast carbs within 30 min", "duration": 10, "facilitator": "Self", "location": "Gym/Home", "prep": "Pre-pack protein powder", "metrics": ["protein_grams", "timing_post_workout"]},
    {"name": "Balanced Lunch", "details": "Mediterranean-style: vegetables, lean protein, olive oil", "duration": 30, "facilitator": "Self", "location": "Home/Office", "prep": "Meal prep on Sunday", "metrics": ["vegetable_servings", "protein_grams", "healthy_fats"]},
    {"name": "Afternoon Healthy Snack", "details": "Nuts, Greek yogurt, or fruit", "duration": 10, "facilitator": "Self", "location": "Anywhere", "prep": "Pack snacks morning", "metrics": ["calories", "satiety_rating"]},
    {"name": "Dinner - High Fiber", "details": "25g fiber target, colorful vegetables", "duration": 40, "facilitator": "Self", "location": "Home", "prep": "Grocery shopping, cooking", "metrics": ["fiber_grams", "vegetable_variety"]},
    {"name": "Evening Supplement", "details": "Zinc, B-complex before bed", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Pill organizer", "metrics": ["supplements_taken"]},
    {"name": "Hydration Check", "details": "Ensure 3L water intake throughout day", "duration": 5, "facilitator": "Self", "location": "Anywhere", "prep": "Fill water bottle", "metrics": ["water_intake_liters"]},
    {"name": "Probiotics Intake", "details": "Morning probiotic for gut health", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Keep refrigerated", "metrics": ["strain_count", "consistency"]},
    {"name": "Collagen Supplement", "details": "Collagen peptides for joint and skin health", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Mix with morning coffee", "metrics": ["grams_consumed"]},
    {"name": "Electrolyte Drink", "details": "LMNT or similar during/after exercise", "duration": 5, "facilitator": "Self", "location": "Gym", "prep": "Pack electrolytes", "metrics": ["sodium_mg", "potassium_mg"]},
    {"name": "Green Smoothie", "details": "Spinach, kale, berries, protein powder", "duration": 10, "facilitator": "Self", "location": "Home", "prep": "Prep ingredients night before", "metrics": ["vegetable_servings", "antioxidant_score"]},
    {"name": "Intermittent Fasting Window", "details": "16:8 protocol - eating window 12pm-8pm", "duration": 0, "facilitator": "Self", "location": "N/A", "prep": "Track fasting app", "metrics": ["fasting_hours", "compliance"]},
    {"name": "Omega-3 Rich Fish Meal", "details": "Salmon or mackerel for EPA/DHA", "duration": 30, "facilitator": "Self", "location": "Home", "prep": "Purchase fresh fish", "metrics": ["omega3_grams", "mercury_consideration"]},
]

# Medication activities
MEDICATION_ACTIVITIES = [
    {"name": "Morning Blood Pressure Medication", "details": "Take with water, before breakfast", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Pill organizer", "metrics": ["time_taken", "blood_pressure_reading"]},
    {"name": "Thyroid Medication", "details": "Empty stomach, 30 min before food", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Set alarm reminder", "metrics": ["time_taken", "empty_stomach_compliance"]},
    {"name": "Metformin with Dinner", "details": "Take with largest meal to reduce GI side effects", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Pill organizer", "metrics": ["time_taken", "meal_size"]},
    {"name": "Statin Before Bed", "details": "Cholesterol medication, evening dose", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Bedside pill organizer", "metrics": ["time_taken", "consistency"]},
    {"name": "Inhaler Use", "details": "Preventive inhaler, morning and evening", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Check inhaler charge", "metrics": ["puffs", "technique_score"]},
    {"name": "Allergy Medication", "details": "Antihistamine as needed during high pollen", "duration": 5, "facilitator": "Self", "location": "Anywhere", "prep": "Carry backup", "metrics": ["symptom_relief_rating"]},
    {"name": "Pain Management Medication", "details": "As prescribed for chronic condition", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Track usage", "metrics": ["pain_level_before", "pain_level_after"]},
    {"name": "Sleep Aid (if needed)", "details": "Melatonin 0.5mg, 30 min before bed", "duration": 5, "facilitator": "Self", "location": "Home", "prep": "Low dose only", "metrics": ["sleep_latency", "sleep_quality"]},
]

# Therapy activities
THERAPY_ACTIVITIES = [
    {"name": "Infrared Sauna Session", "details": "20 min at 140°F for detox and relaxation", "duration": 30, "facilitator": "Spa Staff", "location": "Wellness Center", "equipment": ["infrared_sauna"], "metrics": ["temperature", "duration", "sweat_level"]},
    {"name": "Cold Plunge/Ice Bath", "details": "3-5 min at 50°F for recovery and hormesis", "duration": 10, "facilitator": "Self", "location": "Wellness Center", "equipment": ["cold_plunge_tub"], "metrics": ["water_temp", "duration", "hrv_change"]},
    {"name": "Contrast Therapy", "details": "Alternating hot sauna and cold plunge", "duration": 45, "facilitator": "Spa Staff", "location": "Wellness Center", "equipment": ["sauna", "cold_plunge_tub"], "metrics": ["cycles_completed", "recovery_feeling"]},
    {"name": "Deep Tissue Massage", "details": "Focus on problem areas, pressure as tolerated", "duration": 60, "facilitator": "Massage Therapist", "location": "Spa", "equipment": ["massage_table"], "metrics": ["pressure_level", "areas_treated", "pain_relief"]},
    {"name": "Acupuncture Session", "details": "Traditional Chinese medicine for balance", "duration": 45, "facilitator": "Acupuncturist", "location": "TCM Clinic", "equipment": ["acupuncture_needles"], "metrics": ["points_treated", "energy_level_after"]},
    {"name": "Red Light Therapy", "details": "Full body panel, 10-15 min exposure", "duration": 15, "facilitator": "Self", "location": "Home/Clinic", "equipment": ["red_light_panel"], "metrics": ["exposure_time", "skin_response"]},
    {"name": "Compression Therapy", "details": "Normatec boots for leg recovery", "duration": 30, "facilitator": "Self", "location": "Gym/Home", "equipment": ["compression_boots"], "metrics": ["pressure_setting", "leg_soreness_before_after"]},
    {"name": "Float Tank Session", "details": "Sensory deprivation for mental recovery", "duration": 60, "facilitator": "Float Center Staff", "location": "Float Center", "equipment": ["float_tank"], "metrics": ["relaxation_rating", "mental_clarity"]},
    {"name": "Hyperbaric Oxygen Therapy", "details": "HBOT for cellular recovery", "duration": 60, "facilitator": "HBOT Technician", "location": "HBOT Center", "equipment": ["hyperbaric_chamber"], "metrics": ["pressure_ata", "oxygen_saturation"]},
    {"name": "Cryotherapy Chamber", "details": "Whole body cryo at -200°F for 3 min", "duration": 10, "facilitator": "Cryo Technician", "location": "Cryo Center", "equipment": ["cryo_chamber"], "metrics": ["temperature", "duration", "skin_temp_after"]},
    {"name": "Sound Bath/Meditation", "details": "Guided meditation with singing bowls", "duration": 45, "facilitator": "Sound Healer", "location": "Wellness Center", "equipment": ["singing_bowls"], "metrics": ["relaxation_depth", "stress_reduction"]},
    {"name": "Breathwork Session", "details": "Wim Hof or holotropic breathing", "duration": 30, "facilitator": "Breathwork Coach", "location": "Studio/Home", "equipment": [], "metrics": ["breath_hold_time", "oxygen_saturation"], "remote": True},
]

# Consultation activities
CONSULTATION_ACTIVITIES = [
    {"name": "Cardiologist Check-up", "details": "Annual heart health assessment", "duration": 45, "specialist": "cardiologist", "location": "Cardiology Clinic", "metrics": ["ecg_results", "blood_pressure", "heart_rate"]},
    {"name": "Endocrinologist Consultation", "details": "Hormone panel review and optimization", "duration": 30, "specialist": "endocrinologist", "location": "Endo Clinic", "metrics": ["hormone_levels", "treatment_adjustments"], "remote": True},
    {"name": "Nutritionist Session", "details": "Meal plan review and adjustments", "duration": 45, "allied_health": "dietitian", "location": "Nutrition Office", "metrics": ["macro_targets", "meal_plan_adherence"], "remote": True},
    {"name": "Physical Therapy Session", "details": "Injury rehab and movement optimization", "duration": 60, "allied_health": "physiotherapist", "location": "PT Clinic", "metrics": ["rom_measurements", "strength_tests"]},
    {"name": "Mental Health Check-in", "details": "Therapy session for stress management", "duration": 50, "specialist": "psychiatrist", "location": "Mental Health Clinic", "metrics": ["mood_rating", "anxiety_level", "sleep_quality"], "remote": True},
    {"name": "Dermatologist Appointment", "details": "Skin health check and mole mapping", "duration": 30, "specialist": "dermatologist", "location": "Derm Clinic", "metrics": ["skin_conditions_noted", "uv_damage_assessment"]},
    {"name": "Ophthalmologist Visit", "details": "Comprehensive eye exam", "duration": 45, "specialist": "ophthalmologist", "location": "Eye Clinic", "metrics": ["vision_acuity", "eye_pressure", "retina_health"]},
    {"name": "Sleep Specialist Consultation", "details": "Review sleep study results", "duration": 30, "specialist": "sleep_specialist", "location": "Sleep Clinic", "metrics": ["ahi_score", "sleep_efficiency", "rem_percentage"], "remote": True},
    {"name": "Sports Medicine Consultation", "details": "Athletic performance optimization", "duration": 45, "specialist": "sports_medicine", "location": "Sports Med Clinic", "metrics": ["injury_risk_assessment", "performance_markers"]},
    {"name": "Functional Medicine Doctor", "details": "Root cause analysis and lifestyle medicine", "duration": 60, "specialist": "functional_medicine", "location": "FM Clinic", "metrics": ["biomarker_review", "protocol_adjustments"], "remote": True},
    {"name": "Occupational Therapist Session", "details": "Workplace ergonomics and daily activities", "duration": 45, "allied_health": "occupational_therapist", "location": "OT Clinic", "metrics": ["ergonomic_score", "activity_modifications"]},
    {"name": "Speech Therapist Session", "details": "Voice and swallowing assessment", "duration": 30, "allied_health": "speech_therapist", "location": "Speech Clinic", "metrics": ["voice_quality", "swallow_function"]},
    {"name": "Chiropractor Adjustment", "details": "Spinal alignment and adjustment", "duration": 30, "allied_health": "chiropractor", "location": "Chiro Clinic", "metrics": ["alignment_assessment", "adjustments_made"]},
    {"name": "Health Coach Check-in", "details": "Weekly accountability and goal review", "duration": 30, "allied_health": "health_coach", "location": "Virtual", "metrics": ["goal_progress", "adherence_score"], "remote": True},
]

# Equipment definitions
EQUIPMENT_LIST = [
    {"id": "heart_rate_monitor", "name": "Heart Rate Monitor", "location": "Personal"},
    {"id": "running_watch", "name": "Running GPS Watch", "location": "Personal"},
    {"id": "treadmill", "name": "Treadmill", "location": "Gym"},
    {"id": "barbell", "name": "Olympic Barbell", "location": "Gym"},
    {"id": "dumbbells", "name": "Dumbbell Set", "location": "Gym"},
    {"id": "bench", "name": "Weight Bench", "location": "Gym"},
    {"id": "squat_rack", "name": "Squat Rack", "location": "Gym"},
    {"id": "leg_press", "name": "Leg Press Machine", "location": "Gym"},
    {"id": "yoga_mat", "name": "Yoga Mat", "location": "Personal"},
    {"id": "swim_goggles", "name": "Swimming Goggles", "location": "Personal"},
    {"id": "swim_cap", "name": "Swimming Cap", "location": "Personal"},
    {"id": "bicycle", "name": "Road Bicycle", "location": "Home"},
    {"id": "cycling_computer", "name": "Cycling Computer", "location": "Personal"},
    {"id": "exercise_mat", "name": "Exercise Mat", "location": "Personal"},
    {"id": "foam_roller", "name": "Foam Roller", "location": "Home"},
    {"id": "resistance_bands", "name": "Resistance Bands Set", "location": "Home"},
    {"id": "bosu_ball", "name": "BOSU Balance Ball", "location": "Gym"},
    {"id": "balance_board", "name": "Balance Board", "location": "Gym"},
    {"id": "rowing_machine", "name": "Rowing Machine", "location": "Gym"},
    {"id": "pilates_mat", "name": "Pilates Mat", "location": "Studio"},
    {"id": "pilates_ring", "name": "Pilates Ring", "location": "Studio"},
    {"id": "kettlebells", "name": "Kettlebell Set", "location": "Gym"},
    {"id": "boxing_gloves", "name": "Boxing Gloves", "location": "Boxing Gym"},
    {"id": "heavy_bag", "name": "Heavy Punching Bag", "location": "Boxing Gym"},
    {"id": "fms_kit", "name": "FMS Assessment Kit", "location": "PT Clinic"},
    {"id": "infrared_sauna", "name": "Infrared Sauna", "location": "Wellness Center"},
    {"id": "cold_plunge_tub", "name": "Cold Plunge Tub", "location": "Wellness Center"},
    {"id": "sauna", "name": "Traditional Sauna", "location": "Wellness Center"},
    {"id": "massage_table", "name": "Massage Table", "location": "Spa"},
    {"id": "acupuncture_needles", "name": "Acupuncture Needles", "location": "TCM Clinic"},
    {"id": "red_light_panel", "name": "Red Light Therapy Panel", "location": "Home"},
    {"id": "compression_boots", "name": "Compression Recovery Boots", "location": "Gym"},
    {"id": "float_tank", "name": "Sensory Deprivation Float Tank", "location": "Float Center"},
    {"id": "hyperbaric_chamber", "name": "Hyperbaric Oxygen Chamber", "location": "HBOT Center"},
    {"id": "cryo_chamber", "name": "Cryotherapy Chamber", "location": "Cryo Center"},
    {"id": "singing_bowls", "name": "Singing Bowls Set", "location": "Wellness Center"},
]

# Specialists definitions
SPECIALISTS_LIST = [
    {"id": "cardiologist", "name": "Dr. Sarah Chen", "specialty": "Cardiology", "remote": True},
    {"id": "endocrinologist", "name": "Dr. Michael Ross", "specialty": "Endocrinology", "remote": True},
    {"id": "psychiatrist", "name": "Dr. Emily Watson", "specialty": "Psychiatry", "remote": True},
    {"id": "dermatologist", "name": "Dr. James Park", "specialty": "Dermatology", "remote": False},
    {"id": "ophthalmologist", "name": "Dr. Lisa Thompson", "specialty": "Ophthalmology", "remote": False},
    {"id": "sleep_specialist", "name": "Dr. Robert Kim", "specialty": "Sleep Medicine", "remote": True},
    {"id": "sports_medicine", "name": "Dr. Amanda Garcia", "specialty": "Sports Medicine", "remote": False},
    {"id": "functional_medicine", "name": "Dr. David Lee", "specialty": "Functional Medicine", "remote": True},
]

# Allied Health Professionals definitions
ALLIED_HEALTH_LIST = [
    {"id": "physiotherapist", "name": "Tom Richards", "profession": "Physiotherapist", "remote": False},
    {"id": "dietitian", "name": "Sarah Johnson", "profession": "Registered Dietitian", "remote": True},
    {"id": "occupational_therapist", "name": "Mike Brown", "profession": "Occupational Therapist", "remote": False},
    {"id": "speech_therapist", "name": "Jennifer White", "profession": "Speech-Language Pathologist", "remote": True},
    {"id": "chiropractor", "name": "Dr. Kevin O'Brien", "profession": "Chiropractor", "remote": False},
    {"id": "health_coach", "name": "Rachel Green", "profession": "Certified Health Coach", "remote": True},
    {"id": "massage_therapist", "name": "Chris Taylor", "profession": "Licensed Massage Therapist", "remote": False},
    {"id": "acupuncturist", "name": "Dr. Wei Zhang", "profession": "Licensed Acupuncturist", "remote": False},
]


class DataGenerator:
    """
    Generates realistic test data for the Resource Allocator system.
    
    This class creates:
    - 100+ health activities with proper priorities and dependencies
    - 3 months of availability schedules for all resources
    - Travel plans and client schedule constraints
    """
    
    def __init__(self, start_date: str = "2026-01-15", duration_months: int = 3):
        """
        Initialize the data generator.
        
        Args:
            start_date: Start date for the schedule (YYYY-MM-DD format)
            duration_months: Number of months to generate schedules for
        """
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.duration_months = duration_months
        self.end_date = self.start_date + timedelta(days=duration_months * 30)
        
    def generate_activities(self) -> List[Activity]:
        """
        Generate 100+ realistic health activities.
        
        Activities are assigned priorities based on health importance:
        - Priority 1-20: Critical (medications, essential consultations)
        - Priority 21-50: High (fitness routines, key nutrition)
        - Priority 51-80: Medium (therapy, wellness activities)
        - Priority 81-100: Low (optional supplements, extras)
        
        Returns:
            List of Activity objects
        """
        activities = []
        activity_id = 1
        
        # Generate FITNESS activities (Priority 21-50)
        for i, template in enumerate(FITNESS_ACTIVITIES):
            freq = self._assign_fitness_frequency(template["name"])
            activity = Activity(
                id=f"ACT_{activity_id:03d}",
                name=template["name"],
                activity_type=ActivityType.FITNESS,
                priority=21 + (i % 30),
                frequency=freq,
                duration_minutes=template["duration"],
                details=template["details"],
                facilitator=template["facilitator"],
                location=template["location"],
                can_be_remote=template.get("remote", False),
                prep_requirements=template.get("prep", "Wear appropriate workout clothes"),
                backup_activities=self._get_fitness_backups(template["name"]),
                skip_adjustments="Add extra cardio to next session if skipped",
                metrics_to_collect=template["metrics"],
                equipment_needed=template.get("equipment", []),
                preferred_time_slots=self._get_preferred_slots(template["name"])
            )
            activities.append(activity)
            activity_id += 1
        
        # Generate FOOD activities (Priority 15-40)
        for i, template in enumerate(FOOD_ACTIVITIES):
            freq = self._assign_food_frequency(template["name"])
            activity = Activity(
                id=f"ACT_{activity_id:03d}",
                name=template["name"],
                activity_type=ActivityType.FOOD,
                priority=15 + (i % 25),
                frequency=freq,
                duration_minutes=template["duration"],
                details=template["details"],
                facilitator=template["facilitator"],
                location=template["location"],
                can_be_remote=True,
                prep_requirements=template["prep"],
                backup_activities=[],
                skip_adjustments="Ensure adequate nutrition in next meal",
                metrics_to_collect=template["metrics"],
                preferred_time_slots=self._get_meal_time_slots(template["name"])
            )
            activities.append(activity)
            activity_id += 1
        
        # Generate MEDICATION activities (Priority 1-20 - highest priority)
        for i, template in enumerate(MEDICATION_ACTIVITIES):
            freq = self._assign_medication_frequency(template["name"])
            activity = Activity(
                id=f"ACT_{activity_id:03d}",
                name=template["name"],
                activity_type=ActivityType.MEDICATION,
                priority=1 + (i % 15),
                frequency=freq,
                duration_minutes=template["duration"],
                details=template["details"],
                facilitator=template["facilitator"],
                location=template["location"],
                can_be_remote=True,
                prep_requirements=template["prep"],
                backup_activities=[],
                skip_adjustments="CRITICAL: Take medication as soon as remembered, consult doctor if missed",
                metrics_to_collect=template["metrics"],
                preferred_time_slots=self._get_medication_time_slots(template["name"])
            )
            activities.append(activity)
            activity_id += 1
        
        # Generate THERAPY activities (Priority 51-80)
        for i, template in enumerate(THERAPY_ACTIVITIES):
            freq = self._assign_therapy_frequency(template["name"])
            activity = Activity(
                id=f"ACT_{activity_id:03d}",
                name=template["name"],
                activity_type=ActivityType.THERAPY,
                priority=51 + (i % 30),
                frequency=freq,
                duration_minutes=template["duration"],
                details=template["details"],
                facilitator=template["facilitator"],
                location=template["location"],
                can_be_remote=template.get("remote", False),
                prep_requirements=template.get("prep", "Hydrate well before session"),
                backup_activities=self._get_therapy_backups(template["name"]),
                skip_adjustments="Reschedule within the week if possible",
                metrics_to_collect=template["metrics"],
                equipment_needed=template.get("equipment", []),
                preferred_time_slots=["afternoon", "evening"]
            )
            activities.append(activity)
            activity_id += 1
        
        # Generate CONSULTATION activities (Priority varies by type)
        for i, template in enumerate(CONSULTATION_ACTIVITIES):
            priority = 10 if "Cardiologist" in template["name"] else (30 + (i % 40))
            freq = self._assign_consultation_frequency(template["name"])
            activity = Activity(
                id=f"ACT_{activity_id:03d}",
                name=template["name"],
                activity_type=ActivityType.CONSULTATION,
                priority=priority,
                frequency=freq,
                duration_minutes=template["duration"],
                details=template["details"],
                facilitator=template.get("specialist", template.get("allied_health", "Healthcare Provider")),
                location=template["location"],
                can_be_remote=template.get("remote", False),
                prep_requirements="Prepare questions and health log before appointment",
                backup_activities=[],
                skip_adjustments="Reschedule appointment within 2 weeks",
                metrics_to_collect=template["metrics"],
                specialist_needed=template.get("specialist"),
                allied_health_needed=template.get("allied_health"),
                preferred_time_slots=["morning", "afternoon"]
            )
            activities.append(activity)
            activity_id += 1
        
        # Add more activities to reach 100+
        additional_activities = self._generate_additional_activities(activity_id)
        activities.extend(additional_activities)
        
        return activities
    
    def _generate_additional_activities(self, start_id: int) -> List[Activity]:
        """Generate additional activities to ensure we have 100+."""
        additional = []
        activity_id = start_id
        
        # Add variations of existing activities
        variations = [
            ("Light Recovery Walk", ActivityType.FITNESS, "Easy 20-min walk for active recovery", 20, Frequency.DAILY, 45),
            ("Gratitude Journaling", ActivityType.THERAPY, "Write 3 things grateful for", 10, Frequency.DAILY, 70),
            ("Vitamin B12 Supplement", ActivityType.FOOD, "Sublingual B12 for energy", 5, Frequency.DAILY, 35),
            ("Standing Desk Breaks", ActivityType.FITNESS, "Stand and stretch every hour", 5, Frequency.DAILY, 55),
            ("Evening Wind-Down Routine", ActivityType.THERAPY, "Blue light glasses, dim lights", 15, Frequency.DAILY, 60),
            ("Weekly Progress Photos", ActivityType.FITNESS, "Take body composition photos", 5, Frequency.WEEKLY, 85),
            ("Blood Glucose Check", ActivityType.MEDICATION, "Morning fasting glucose test", 5, Frequency.DAILY, 5),
            ("Posture Check-ins", ActivityType.FITNESS, "Ergonomic posture assessment", 5, Frequency.THREE_TIMES_WEEKLY, 65),
            ("Social Connection Time", ActivityType.THERAPY, "Quality time with family/friends", 60, Frequency.WEEKLY, 75),
            ("Nature Exposure", ActivityType.THERAPY, "Outdoor time in natural setting", 30, Frequency.WEEKLY, 80),
            ("Brain Training Games", ActivityType.FITNESS, "Cognitive exercises app", 15, Frequency.DAILY, 70),
            ("Grip Strength Training", ActivityType.FITNESS, "Hand gripper exercises", 10, Frequency.THREE_TIMES_WEEKLY, 50),
            ("Neck and Shoulder Stretches", ActivityType.FITNESS, "Office-friendly stretches", 10, Frequency.DAILY, 55),
            ("Magnesium Bath Soak", ActivityType.THERAPY, "Epsom salt bath for recovery", 30, Frequency.TWICE_WEEKLY, 72),
            ("Meal Prep Sunday", ActivityType.FOOD, "Prepare healthy meals for week", 120, Frequency.WEEKLY, 30),
            # Additional activities to reach 100+
            ("Ankle Mobility Drills", ActivityType.FITNESS, "Circles and stretches for ankle health", 10, Frequency.DAILY, 58),
            ("Hip Flexor Stretches", ActivityType.FITNESS, "Combat sitting with hip openers", 10, Frequency.DAILY, 56),
            ("Wrist Exercises", ActivityType.FITNESS, "Prevent RSI with wrist mobility", 5, Frequency.DAILY, 60),
            ("Deep Breathing Exercises", ActivityType.THERAPY, "4-7-8 breathing technique", 10, Frequency.TWICE_DAILY, 65),
            ("Cold Shower Ending", ActivityType.THERAPY, "30 seconds cold at end of shower", 5, Frequency.DAILY, 68),
            ("Foam Rolling Session", ActivityType.FITNESS, "Self-myofascial release", 15, Frequency.DAILY, 52),
            ("Meditation Session", ActivityType.THERAPY, "Guided mindfulness meditation", 15, Frequency.DAILY, 62),
            ("Vitamin C Intake", ActivityType.FOOD, "Citrus or supplement for immunity", 5, Frequency.DAILY, 38),
            ("Fiber Supplement", ActivityType.FOOD, "Psyllium husk for digestive health", 5, Frequency.DAILY, 40),
            ("Apple Cider Vinegar", ActivityType.FOOD, "Diluted ACV before meals", 5, Frequency.DAILY, 42),
            ("Evening Protein Snack", ActivityType.FOOD, "Casein or cottage cheese before bed", 10, Frequency.DAILY, 36),
            ("Mid-Day Walk", ActivityType.FITNESS, "10-minute walk after lunch", 10, Frequency.DAILY, 48),
            ("Stair Intervals", ActivityType.FITNESS, "Quick stair climbing for cardio", 10, Frequency.THREE_TIMES_WEEKLY, 46),
            ("Jump Rope Session", ActivityType.FITNESS, "Cardio and coordination training", 15, Frequency.THREE_TIMES_WEEKLY, 44),
            ("Wall Sits", ActivityType.FITNESS, "Isometric leg strengthening", 5, Frequency.DAILY, 54),
            ("Plank Challenge", ActivityType.FITNESS, "Progressive plank hold times", 5, Frequency.DAILY, 53),
            ("Box Breathing", ActivityType.THERAPY, "4-4-4-4 breath pattern for stress", 10, Frequency.DAILY, 66),
            ("Progressive Muscle Relaxation", ActivityType.THERAPY, "Full body tension release", 15, Frequency.DAILY, 64),
            ("Sleep Hygiene Review", ActivityType.THERAPY, "Check bedroom environment", 10, Frequency.WEEKLY, 74),
            ("Weekly Weigh-in", ActivityType.FITNESS, "Track body composition", 5, Frequency.WEEKLY, 86),
            ("Blood Pressure Log", ActivityType.MEDICATION, "Record BP readings", 5, Frequency.DAILY, 8),
        ]
        
        for name, activity_type, details, duration, freq, priority in variations:
            activity = Activity(
                id=f"ACT_{activity_id:03d}",
                name=name,
                activity_type=activity_type,
                priority=priority,
                frequency=freq,
                duration_minutes=duration,
                details=details,
                facilitator="Self",
                location="Home",
                can_be_remote=True,
                prep_requirements="",
                backup_activities=[],
                skip_adjustments="Resume on next scheduled day",
                metrics_to_collect=["completion", "quality_rating"],
                preferred_time_slots=["morning"] if "Morning" in name else ["evening"] if "Evening" in name else ["morning", "afternoon", "evening"]
            )
            additional.append(activity)
            activity_id += 1
        
        return additional
    
    def _assign_fitness_frequency(self, name: str) -> Frequency:
        """Assign appropriate frequency to fitness activities."""
        if "Daily" in name or "Eye" in name or "Mobility" in name:
            return Frequency.DAILY
        elif "HIIT" in name or "Interval" in name:
            return Frequency.TWICE_WEEKLY
        elif "Strength" in name:
            return Frequency.THREE_TIMES_WEEKLY
        elif "Yoga" in name or "Swimming" in name:
            return Frequency.TWICE_WEEKLY
        else:
            return Frequency.THREE_TIMES_WEEKLY
    
    def _assign_food_frequency(self, name: str) -> Frequency:
        """Assign appropriate frequency to food/nutrition activities."""
        if "Breakfast" in name or "Lunch" in name or "Dinner" in name:
            return Frequency.DAILY
        elif "Supplement" in name or "Hydration" in name:
            return Frequency.DAILY
        elif "Omega-3" in name or "Fish" in name:
            return Frequency.TWICE_WEEKLY
        else:
            return Frequency.DAILY
    
    def _assign_medication_frequency(self, name: str) -> Frequency:
        """Assign appropriate frequency to medication activities."""
        if "Inhaler" in name:
            return Frequency.TWICE_DAILY
        elif "As needed" in name.lower() or "if needed" in name.lower():
            return Frequency.AS_NEEDED
        else:
            return Frequency.DAILY
    
    def _assign_therapy_frequency(self, name: str) -> Frequency:
        """Assign appropriate frequency to therapy activities."""
        if "Massage" in name:
            return Frequency.WEEKLY
        elif "Sauna" in name or "Cold Plunge" in name:
            return Frequency.THREE_TIMES_WEEKLY
        elif "Breathwork" in name:
            return Frequency.DAILY
        else:
            return Frequency.WEEKLY
    
    def _assign_consultation_frequency(self, name: str) -> Frequency:
        """Assign appropriate frequency to consultation activities."""
        if "Check-in" in name or "Coach" in name:
            return Frequency.WEEKLY
        elif "Physical Therapy" in name or "Chiro" in name:
            return Frequency.WEEKLY
        else:
            return Frequency.MONTHLY
    
    def _get_fitness_backups(self, name: str) -> List[str]:
        """Get backup activities for fitness activities."""
        if "Run" in name or "Cardio" in name:
            return ["ACT_007"]  # Cycling as backup
        elif "Strength" in name:
            return ["ACT_012"]  # Resistance band training
        elif "Swimming" in name:
            return ["ACT_001"]  # Running as backup
        return []
    
    def _get_therapy_backups(self, name: str) -> List[str]:
        """Get backup activities for therapy activities."""
        if "Sauna" in name:
            return ["ACT_044"]  # Hot bath as backup
        elif "Cold Plunge" in name:
            return []  # Cold shower at home
        return []
    
    def _get_preferred_slots(self, name: str) -> List[str]:
        """Get preferred time slots for fitness activities."""
        if "Morning" in name:
            return ["morning"]
        elif "Evening" in name:
            return ["evening"]
        elif "HIIT" in name or "Strength" in name:
            return ["morning", "afternoon"]
        return ["morning", "afternoon", "evening"]
    
    def _get_meal_time_slots(self, name: str) -> List[str]:
        """Get preferred time slots for food activities."""
        if "Breakfast" in name or "Morning" in name:
            return ["morning"]
        elif "Lunch" in name or "Mid-day" in name or "Afternoon" in name:
            return ["afternoon"]
        elif "Dinner" in name or "Evening" in name:
            return ["evening"]
        elif "Pre-Workout" in name:
            return ["morning", "afternoon"]
        elif "Post-Workout" in name:
            return ["morning", "afternoon", "evening"]
        return ["morning", "afternoon", "evening"]
    
    def _get_medication_time_slots(self, name: str) -> List[str]:
        """Get preferred time slots for medication activities."""
        if "Morning" in name or "Thyroid" in name:
            return ["morning"]
        elif "Bed" in name or "Evening" in name or "Sleep" in name:
            return ["evening"]
        elif "Dinner" in name:
            return ["evening"]
        return ["morning"]
    
    def generate_equipment_availability(self) -> List[Equipment]:
        """
        Generate equipment with 3-month availability schedules.
        
        Personal equipment is always available.
        Shared equipment (gym, wellness center) has scheduled availability.
        
        Returns:
            List of Equipment objects with availability schedules
        """
        equipment_list = []
        
        for eq_data in EQUIPMENT_LIST:
            availability = []
            current_date = self.start_date
            
            while current_date < self.end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                weekday = current_date.weekday()
                
                # Personal equipment always available
                if eq_data["location"] == "Personal" or eq_data["location"] == "Home":
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="06:00",
                        end_time="22:00",
                        is_available=True
                    ))
                # Gym equipment available 6am-10pm, closed Sundays
                elif eq_data["location"] == "Gym":
                    is_available = weekday != 6  # Closed Sunday
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="06:00",
                        end_time="22:00",
                        is_available=is_available,
                        notes="Gym closed on Sundays" if not is_available else ""
                    ))
                # Wellness centers have more limited hours
                elif "Wellness" in eq_data["location"] or "Center" in eq_data["location"]:
                    is_available = weekday < 6  # Mon-Sat only
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="09:00",
                        end_time="20:00",
                        is_available=is_available,
                        notes="Closed weekends" if not is_available else ""
                    ))
                else:
                    # Default clinic/studio hours
                    is_available = weekday < 5  # Mon-Fri only
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="08:00",
                        end_time="18:00",
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
        """
        Generate specialists with realistic 3-month availability schedules.
        
        Specialists typically work limited hours with varying schedules.
        
        Returns:
            List of Specialist objects with availability schedules
        """
        specialists = []
        
        for spec_data in SPECIALISTS_LIST:
            availability = []
            current_date = self.start_date
            
            # Each specialist has their own working days (Mon-Fri, some variation)
            working_days = random.sample([0, 1, 2, 3, 4], k=random.randint(3, 5))
            
            while current_date < self.end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                weekday = current_date.weekday()
                
                # Check if it's a working day for this specialist
                is_working_day = weekday in working_days
                
                # Add some random time off (vacation, conferences)
                random_off = random.random() < 0.05  # 5% chance of being off
                
                is_available = is_working_day and not random_off
                
                if is_available:
                    # Morning and afternoon slots
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="09:00",
                        end_time="12:00",
                        is_available=True,
                        notes="Morning appointments"
                    ))
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="14:00",
                        end_time="17:00",
                        is_available=True,
                        notes="Afternoon appointments"
                    ))
                else:
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="09:00",
                        end_time="17:00",
                        is_available=False,
                        notes="Not available" if not is_working_day else "Out of office"
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
        """
        Generate allied health professionals with 3-month availability.
        
        Allied health professionals typically have more flexible schedules
        than specialists but still have specific working hours.
        
        Returns:
            List of AlliedHealth objects with availability schedules
        """
        allied_health = []
        
        for ah_data in ALLIED_HEALTH_LIST:
            availability = []
            current_date = self.start_date
            
            # Allied health typically works 4-5 days per week
            working_days = random.sample([0, 1, 2, 3, 4, 5], k=random.randint(4, 5))
            
            while current_date < self.end_date:
                date_str = current_date.strftime("%Y-%m-%d")
                weekday = current_date.weekday()
                
                is_working_day = weekday in working_days
                random_off = random.random() < 0.03  # 3% chance of being off
                
                is_available = is_working_day and not random_off
                
                if is_available:
                    # Full day availability in slots
                    for start_hour, end_hour in [(8, 12), (13, 17)]:
                        availability.append(TimeSlot(
                            date=date_str,
                            start_time=f"{start_hour:02d}:00",
                            end_time=f"{end_hour:02d}:00",
                            is_available=True
                        ))
                else:
                    availability.append(TimeSlot(
                        date=date_str,
                        start_time="08:00",
                        end_time="17:00",
                        is_available=False,
                        notes="Not available"
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
        """
        Generate realistic travel plans for the 3-month period.
        
        Includes business trips and personal travel that affect scheduling.
        
        Returns:
            List of TravelPlan objects
        """
        travel_plans = [
            TravelPlan(
                id="TRAVEL_001",
                destination="New York City",
                start_date=(self.start_date + timedelta(days=15)).strftime("%Y-%m-%d"),
                end_date=(self.start_date + timedelta(days=18)).strftime("%Y-%m-%d"),
                timezone="America/New_York",
                notes="Business conference - limited gym access, hotel gym available"
            ),
            TravelPlan(
                id="TRAVEL_002",
                destination="Hawaii",
                start_date=(self.start_date + timedelta(days=45)).strftime("%Y-%m-%d"),
                end_date=(self.start_date + timedelta(days=52)).strftime("%Y-%m-%d"),
                timezone="Pacific/Honolulu",
                notes="Family vacation - beach activities can substitute for gym workouts"
            ),
            TravelPlan(
                id="TRAVEL_003",
                destination="London",
                start_date=(self.start_date + timedelta(days=75)).strftime("%Y-%m-%d"),
                end_date=(self.start_date + timedelta(days=79)).strftime("%Y-%m-%d"),
                timezone="Europe/London",
                notes="Work trip - telehealth appointments still possible"
            ),
        ]
        return travel_plans
    
    def generate_client_schedule(self) -> ClientSchedule:
        """
        Generate a realistic client schedule with blocked times and preferences.
        
        Returns:
            ClientSchedule object with blocked times and preferences
        """
        blocked_times = []
        current_date = self.start_date
        
        while current_date < self.end_date:
            date_str = current_date.strftime("%Y-%m-%d")
            weekday = current_date.weekday()
            
            # Work hours blocked (9am-5pm Mon-Fri)
            if weekday < 5:
                blocked_times.append(TimeSlot(
                    date=date_str,
                    start_time="09:00",
                    end_time="17:00",
                    is_available=False,
                    notes="Work hours"
                ))
            
            current_date += timedelta(days=1)
        
        client_schedule = ClientSchedule(
            blocked_times=blocked_times,
            preferred_workout_times=["morning", "evening"],
            preferred_meal_times={
                "breakfast": "07:30",
                "lunch": "12:30",
                "dinner": "19:00",
                "snack": "15:30"
            },
            wake_time="06:00",
            sleep_time="22:30"
        )
        
        return client_schedule
    
    def save_all_data(self, output_dir: str = "data"):
        """
        Generate and save all test data to JSON and CSV files.
        
        Args:
            output_dir: Directory to save the data files
        """
        print("Generating activities...")
        activities = self.generate_activities()
        
        print("Generating equipment availability...")
        equipment = self.generate_equipment_availability()
        
        print("Generating specialist availability...")
        specialists = self.generate_specialist_availability()
        
        print("Generating allied health availability...")
        allied_health = self.generate_allied_health_availability()
        
        print("Generating travel plans...")
        travel_plans = self.generate_travel_plans()
        
        print("Generating client schedule...")
        client_schedule = self.generate_client_schedule()
        
        # Save activities to JSON
        activities_data = [a.to_dict() for a in activities]
        with open(f"{output_dir}/activities.json", "w") as f:
            json.dump(activities_data, f, indent=2)
        
        # Save activities to CSV
        self._save_activities_csv(activities, f"{output_dir}/activities.csv")
        
        # Save equipment to JSON
        equipment_data = [e.to_dict() for e in equipment]
        with open(f"{output_dir}/equipment.json", "w") as f:
            json.dump(equipment_data, f, indent=2)
        
        # Save specialists to JSON
        specialists_data = [s.to_dict() for s in specialists]
        with open(f"{output_dir}/specialists.json", "w") as f:
            json.dump(specialists_data, f, indent=2)
        
        # Save allied health to JSON
        allied_health_data = [ah.to_dict() for ah in allied_health]
        with open(f"{output_dir}/allied_health.json", "w") as f:
            json.dump(allied_health_data, f, indent=2)
        
        # Save travel plans to JSON
        travel_plans_data = [tp.to_dict() for tp in travel_plans]
        with open(f"{output_dir}/travel_plans.json", "w") as f:
            json.dump(travel_plans_data, f, indent=2)
        
        # Save client schedule to JSON
        with open(f"{output_dir}/client_schedule.json", "w") as f:
            json.dump(client_schedule.to_dict(), f, indent=2)
        
        print(f"\nGenerated {len(activities)} activities")
        print(f"Generated {len(equipment)} equipment items with 3-month availability")
        print(f"Generated {len(specialists)} specialists with schedules")
        print(f"Generated {len(allied_health)} allied health professionals with schedules")
        print(f"Generated {len(travel_plans)} travel plans")
        print(f"All data saved to {output_dir}/")
        
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
                # Convert lists to strings for CSV
                row["backup_activities"] = "|".join(row["backup_activities"])
                row["metrics_to_collect"] = "|".join(row["metrics_to_collect"])
                row["equipment_needed"] = "|".join(row["equipment_needed"])
                row["preferred_time_slots"] = "|".join(row["preferred_time_slots"])
                writer.writerow(row)


if __name__ == "__main__":
    # Generate all test data
    generator = DataGenerator(start_date="2026-01-15", duration_months=3)
    generator.save_all_data("data")
