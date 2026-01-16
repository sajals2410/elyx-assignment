# Streamlit App - Resource Allocator

## 🚀 Running the Streamlit App

### Quick Start

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

   Or use the helper script:
   ```bash
   ./run_app.sh
   ```

3. **Open your browser:**
   The app will automatically open at `http://localhost:8501`

### Features

The Streamlit app provides:

- **📅 Schedule Configuration**
  - Set start date
  - Choose number of weeks to schedule
  - Regenerate test data if needed

- **📊 Statistics Dashboard**
  - Total activities scheduled
  - Breakdown by type (Fitness, Food, Medication, Therapy, Consultation)
  - Breakdown by priority (Critical, High, Medium, Low)
  - Backup activities used

- **📋 Schedule Preview**
  - View activities by date
  - Detailed activity information
  - Time slots and durations

- **💾 Download Outputs**
  - Text calendar (.txt)
  - HTML calendar (.html)
  - iCalendar file (.ics) - for importing to calendar apps
  - JSON summary (.json)

- **👀 HTML Calendar Viewer**
  - View the generated HTML calendar directly in the app

### Usage

1. Configure settings in the sidebar
2. Click "🚀 Generate Schedule"
3. Wait for the schedule to be generated
4. View statistics and preview
5. Download outputs as needed

### Troubleshooting

If you encounter issues:

1. **Make sure virtual environment is activated:**
   ```bash
   source venv/bin/activate
   ```

2. **Check if all dependencies are installed:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify data directory exists:**
   ```bash
   ls data/
   ```
   If it doesn't exist, the app will generate it automatically.

4. **Check Streamlit version:**
   ```bash
   streamlit --version
   ```

### Stopping the App

Press `Ctrl+C` in the terminal to stop the Streamlit server.
