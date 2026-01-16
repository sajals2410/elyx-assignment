# Resource Allocator - Quick Command Reference

## 🚀 Quick Start Commands

### 1. Activate Virtual Environment
```bash
cd /Users/sajalsingh/Desktop/projectelyx
source venv/bin/activate
```

### 2. Run the Scheduler (Command Line)

**Basic run (2 weeks, default settings):**
```bash
python main.py --weeks 2
```

**Custom settings:**
```bash
python main.py --weeks 4 --start-date 2026-02-01 --sample-days 7
```

**Only generate test data:**
```bash
python main.py --generate-only
```

**Only run scheduler (data must exist):**
```bash
python main.py --schedule-only --weeks 2
```

**No console preview:**
```bash
python main.py --weeks 2 --no-preview
```

### 3. Run Streamlit Web App

**Start the app:**
```bash
streamlit run app.py
```
Then open: http://localhost:8501

**Or use the helper script:**
```bash
./run_app.sh
```

**Stop the Streamlit server:**
Press `Ctrl+C` in the terminal, or:
```bash
pkill -f streamlit
```

### 4. View Generated Outputs

**View HTML calendar in browser:**
```bash
open output/schedule.html
```

**View text schedule:**
```bash
cat output/schedule_text.txt
```

**View JSON summary (formatted):**
```bash
cat output/schedule_summary.json | python -m json.tool
```

**View scheduling log:**
```bash
cat output/scheduling_log.txt
```

**View first 50 lines of text schedule:**
```bash
head -50 output/schedule_text.txt
```

### 5. Data Management

**Regenerate all test data:**
```bash
python main.py --generate-only
```

**Check what data files exist:**
```bash
ls -lh data/
```

**Check output files:**
```bash
ls -lh output/
```

### 6. Development & Testing

**Test imports:**
```bash
python -c "import models; import scheduler; import calendar_output; print('✓ All modules OK')"
```

**Run scheduler directly (Python):**
```bash
python -c "from scheduler import load_data, ResourceAllocator; \
activities, equipment, specialists, allied_health, travel_plans, client_schedule = load_data('data'); \
scheduler = ResourceAllocator(activities, equipment, specialists, allied_health, travel_plans, client_schedule, '2026-01-15', '2026-01-29'); \
schedule = scheduler.generate_schedule(); \
print(f'Scheduled {len(schedule)} activities')"
```

**Check Python version:**
```bash
python --version
```

**Check installed packages:**
```bash
pip list
```

### 7. Useful One-Liners

**Full workflow (generate data + schedule + view):**
```bash
python main.py --weeks 2 && open output/schedule.html
```

**Quick test (1 week, no preview):**
```bash
python main.py --weeks 1 --no-preview
```

**Generate 4-week schedule and show stats:**
```bash
python main.py --weeks 4 --no-preview && cat output/schedule_summary.json | python -m json.tool | grep -A 10 statistics
```

**Count activities by type:**
```bash
cat output/schedule_summary.json | python -m json.tool | grep -A 5 "by_type"
```

### 8. Troubleshooting

**Reinstall dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

**Check if virtual environment is active:**
```bash
which python
# Should show: /Users/sajalsingh/Desktop/projectelyx/venv/bin/python
```

**Deactivate virtual environment:**
```bash
deactivate
```

**Clear output files:**
```bash
rm -f output/*.txt output/*.html output/*.ics output/*.json
```

**Clear all generated data:**
```bash
rm -rf data/*.json data/*.csv
```

### 9. Streamlit App Commands

**Run on specific port:**
```bash
streamlit run app.py --server.port 8502
```

**Run with custom theme:**
```bash
streamlit run app.py --theme.base dark
```

**View Streamlit config:**
```bash
streamlit config show
```

### 10. File Operations

**Copy schedule to Desktop:**
```bash
cp output/schedule.ics ~/Desktop/
```

**Open all output files:**
```bash
open output/
```

**View file sizes:**
```bash
du -h output/*
```

---

## 📋 Common Workflows

### Workflow 1: Quick Test
```bash
source venv/bin/activate
python main.py --weeks 1 --no-preview
open output/schedule.html
```

### Workflow 2: Full Schedule Generation
```bash
source venv/bin/activate
python main.py --weeks 12 --start-date 2026-01-15
```

### Workflow 3: Use Streamlit App
```bash
source venv/bin/activate
streamlit run app.py
# Then open browser to http://localhost:8501
```

### Workflow 4: Generate and Export
```bash
source venv/bin/activate
python main.py --weeks 4 --no-preview
cp output/schedule.ics ~/Desktop/my_schedule.ics
open output/schedule.html
```

---

## 💡 Tips

- Always activate the virtual environment first: `source venv/bin/activate`
- Use `--no-preview` for faster execution when you don't need console output
- The HTML calendar is the best way to view the full schedule visually
- The .ics file can be imported into Google Calendar, Apple Calendar, or Outlook
- Check `output/scheduling_log.txt` for detailed scheduling decisions
