import React, { useState, useEffect } from 'react';
import { apiService, ScheduleData, Statistics } from './api';
import ConfigPanel from './components/ConfigPanel';
import StatisticsDashboard from './components/StatisticsDashboard';
import ScheduleViewer from './components/ScheduleViewer';
import DownloadPanel from './components/DownloadPanel';
import './App.css';

function App() {
  const [loading, setLoading] = useState(false);
  const [scheduleData, setScheduleData] = useState<ScheduleData | null>(null);
  const [statistics, setStatistics] = useState<Statistics | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [apiConnected, setApiConnected] = useState(false);

  useEffect(() => {
    // Check API connection on mount
    apiService.healthCheck().then((connected) => {
      setApiConnected(connected);
      if (connected) {
        loadSchedule();
      } else {
        setError('Cannot connect to API. Make sure the Flask server is running on port 5000.');
      }
    });
  }, []);

  const loadSchedule = async () => {
    try {
      const data = await apiService.getSchedule();
      if (data) {
        setScheduleData(data);
        setStatistics(data.statistics);
        setError(null);
      }
    } catch (err) {
      console.error('Failed to load schedule:', err);
    }
  };

  const handleGenerate = async (startDate: string, weeks: number, regenerateData: boolean) => {
    setLoading(true);
    setError(null);

    try {
      // Generate data if needed
      if (regenerateData) {
        const dataResult = await apiService.generateData(startDate, 3);
        if (!dataResult.success) {
          throw new Error(dataResult.error || 'Failed to generate data');
        }
      }

      // Generate schedule
      const result = await apiService.generateSchedule(startDate, weeks);
      if (!result.success) {
        throw new Error(result.error || 'Failed to generate schedule');
      }

      // Reload schedule data
      await loadSchedule();
    } catch (err: any) {
      setError(err.message || 'An error occurred while generating the schedule');
      console.error('Generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-content">
          <h1>🏥 Resource Allocator</h1>
          <p className="subtitle">Transform Health Recommendations into Personalized Schedules</p>
          <div className={`api-status ${apiConnected ? 'connected' : 'disconnected'}`}>
            {apiConnected ? '🟢 API Connected' : '🔴 API Disconnected'}
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          {error && (
            <div className="error-message">
              <strong>Error:</strong> {error}
            </div>
          )}

          <ConfigPanel onGenerate={handleGenerate} loading={loading} />

          {statistics && (
            <>
              <StatisticsDashboard statistics={statistics} />
              {scheduleData && (
                <ScheduleViewer schedule={scheduleData.schedule} />
              )}
              <DownloadPanel />
            </>
          )}

          {!statistics && !loading && (
            <div className="welcome-message">
              <h2>👋 Welcome to Resource Allocator!</h2>
              <p>Configure your schedule settings above and click "Generate Schedule" to get started.</p>
              <p>The system will create a personalized schedule respecting all constraints including:</p>
              <ul>
                <li>Equipment availability</li>
                <li>Specialist schedules</li>
                <li>Client work hours and preferences</li>
                <li>Travel plans</li>
              </ul>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>Resource Allocator - Health Activity Scheduler</p>
      </footer>
    </div>
  );
}

export default App;
