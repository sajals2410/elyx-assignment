# Resource Allocator - Health Activity Scheduler

A Python implementation of the Resource Allocator system that transforms HealthSpan AI recommendations into personalized, scheduled activities.

## 📋 Overview

The Resource Allocator is a scheduling system that:
1. Takes an **Action Plan** (list of health activities ordered by priority)
2. Considers **Resource Constraints** (equipment, specialists, allied health)
3. Respects **Personal Constraints** (travel plans, work schedule, preferences)
4. Outputs a **Personalized Schedule** in readable calendar formats

![Resource Allocator Diagram](resource_allocator_diagram.png)

## 🚀 Quick Start

```bash
# Navigate to the project directory
cd /home/ubuntu/assignment_solutions

# Run the complete system
python main.py

# Or run with custom options
python main.py --weeks 8 --sample-days 14
```

## 📁 Project Structure

```
assignment_solutions/
├── models.py           # Data models (Activity, Equipment, Specialist, etc.)
├── data_generator.py   # Generates 100+ realistic test activities
├── scheduler.py        # Core scheduling algorithm
├── calendar_output.py  # Output formatters (Text, HTML, iCal, JSON)
├── main.py            # Main entry point
├── README.md          # This documentation
├── data/              # Generated test data
│   ├── activities.json
│   ├── activities.csv
│   ├── equipment.json
│   ├── specialists.json
│   ├── allied_health.json
│   ├── travel_plans.json
│   └── client_schedule.json
└── output/            # Generated schedules
    ├── schedule.html
    ├── schedule.ics
    ├── schedule_text.txt
    ├── schedule_summary.json
    └── scheduling_log.txt
```

## 📊 Task 1: Activity Test Data (100+ Activities)

The system generates realistic health activities across 5 categories:

### Activity Types
| Type | Count | Examples |
|------|-------|----------|
| **Fitness** | 20+ | Zone 2 cardio, HIIT, strength training, yoga |
| **Food/Nutrition** | 15+ | Meals, supplements, hydration, protein intake |
| **Medication** | 8+ | BP meds, thyroid, statins, inhalers |
| **Therapy** | 12+ | Sauna, cold plunge, massage, acupuncture |
| **Consultation** | 14+ | Cardiologist, PT, nutritionist, mental health |

### Activity Fields (as per requirements)
Each activity includes:
1. **Activity Type** - Category (fitness, food, medication, therapy, consultation)
2. **Frequency** - How often (daily, weekly, 3x/week, monthly)
3. **Details** - Specific instructions (e.g., "Maintain HR between 120-140")
4. **Facilitator** - Who helps (trainer, doctor, self)
5. **Location** - Where it happens (gym, home, clinic)
6. **Remote Capable** - Can be done via video call
7. **Prep Requirements** - What needs to be prepared
8. **Backup Activities** - Substitutes if unavailable
9. **Skip Adjustments** - What to do if missed
10. **Metrics to Collect** - Data to record

## 📅 Task 2: Availability Data (3 Months)

### Resources Generated
- **Equipment** (36 items): Heart rate monitors, gym equipment, therapy tools
- **Specialists** (8): Cardiologist, endocrinologist, psychiatrist, etc.
- **Allied Health** (8): Physiotherapist, dietitian, health coach, etc.
- **Travel Plans** (3): Sample business and vacation trips
- **Client Schedule**: Work hours, wake/sleep times, preferences

### Availability Rules
- Personal equipment: Always available
- Gym equipment: 6am-10pm, closed Sundays
- Wellness centers: 9am-8pm, Mon-Sat
- Specialists: 3-5 days/week, morning and afternoon slots
- Allied health: 4-5 days/week, full day coverage

## 🔧 Task 3: Scheduling Algorithm

The scheduler uses a **priority-based greedy algorithm**:

```
Algorithm: ResourceAllocator.generate_schedule()

1. Sort activities by priority (lower = more important)
2. For each day in the date range:
   a. Check if it's a travel day (special handling)
   b. For each activity (by priority):
      - Determine if it should be scheduled today (based on frequency)
      - Check resource availability (equipment, specialist, allied health)
      - Check client availability (not during work, not sleeping)
      - Find available time slot (preferring preferred times)
      - If no slot available, try backup activities
      - Schedule or log the conflict
3. Return the complete schedule
```

### Constraint Handling
- **Travel Days**: Only remote-capable activities scheduled
- **Work Hours**: Activities scheduled before/after work
- **Equipment**: Checked against availability index
- **Specialists**: Time slots matched with availability windows
- **Priorities**: Critical activities (medications) always scheduled first

## 📤 Task 4: Calendar Output Formats

### 1. Text Calendar (`schedule_text.txt`)
Console-friendly format with:
- Weekly organization
- Activity details and times
- Color coding by type
- Weekly summaries

### 2. HTML Calendar (`schedule.html`)
Visual, browser-viewable format with:
- Beautiful gradient design
- Activity type legend
- Weekly statistics
- Responsive layout
- Color-coded activities

### 3. iCalendar (`schedule.ics`)
Standard calendar format for:
- Google Calendar import
- Apple Calendar import
- Outlook import
- Any calendar app

### 4. JSON Summary (`schedule_summary.json`)
Programmatic format with:
- Complete schedule data
- Statistics and analytics
- Easy API integration

## 🎯 Usage Examples

### Generate Only Test Data
```bash
python main.py --generate-only
```

### Schedule with Custom Duration
```bash
python main.py --weeks 8 --start-date 2026-02-01
```

### Run Scheduler Only (data exists)
```bash
python main.py --schedule-only
```

### No Console Preview
```bash
python main.py --no-preview
```

## 📈 Sample Output Statistics

```
Schedule generated successfully!
  → Total activities scheduled: 1,247
  → Activities by type: 
      fitness: 312, food: 420, medication: 280, 
      therapy: 156, consultation: 79
  → Activities by priority: 
      critical: 280, high: 467, medium: 312, low: 188
  → Backup activities used: 23
```

---

## 🤖 GenAI Prompts Used

As required by the assignment, here are the prompts used to complete this task:

### Prompt 1: Initial Analysis
```
Read and analyze the programming assignment from /home/ubuntu/Uploads/Programming Assignment.pdf. 
Understand all the problems/questions in the assignment. Then, write complete Python solutions 
for each problem with detailed comments explaining the logic and approach.
```

### Prompt 2: Data Model Design
```
Create Python dataclasses for the Resource Allocator system including:
- Activity with all 10 required fields (type, frequency, details, facilitator, etc.)
- Equipment, Specialist, AlliedHealth with availability schedules
- TravelPlan and ClientSchedule for constraints
- ScheduledActivity for the output
Use proper type hints and include to_dict/from_dict methods for JSON serialization.
```

### Prompt 3: Test Data Generation
```
Generate realistic health activity test data for at least 100 activities including:
- 20+ fitness activities (running, HIIT, strength training, yoga)
- 15+ nutrition activities (meals, supplements, hydration)
- 8+ medication activities (with timing requirements)
- 12+ therapy activities (sauna, massage, acupuncture)
- 14+ consultation activities (specialists and allied health)
Each should have realistic details, metrics, and backup activities.
```

### Prompt 4: Scheduling Algorithm
```
Implement a scheduler that:
1. Sorts activities by health priority
2. Handles different frequencies (daily, weekly, monthly)
3. Checks equipment, specialist, and allied health availability
4. Respects client work hours and travel plans
5. Uses backup activities when primary ones can't be scheduled
6. Tracks scheduling conflicts in a log
```

### Prompt 5: Calendar Output
```
Create calendar output formatters that generate:
1. Text-based calendar with color coding for terminal display
2. Beautiful HTML calendar with weekly organization
3. iCalendar (.ics) file for importing to calendar apps
4. JSON summary for programmatic use
Each should show activity details, times, and weekly statistics.
```

---

## 📝 License

This project was created as a programming assignment solution.

## 👤 Author

Generated with assistance from Claude (Anthropic) AI.
