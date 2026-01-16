import React, { useState } from 'react';
import { format, parseISO } from 'date-fns';
import { ScheduleActivity } from '../api';
import './ScheduleViewer.css';

interface ScheduleViewerProps {
  schedule: Record<string, ScheduleActivity[]> | null;
}

const ScheduleViewer: React.FC<ScheduleViewerProps> = ({ schedule }) => {
  const [selectedDate, setSelectedDate] = useState<string | null>(null);

  if (!schedule || Object.keys(schedule).length === 0) {
    return (
      <div className="schedule-viewer">
        <p>No schedule available. Generate a schedule first.</p>
      </div>
    );
  }

  const dates = Object.keys(schedule).sort();
  const displayDate = selectedDate || dates[0];
  const dayActivities = schedule[displayDate] || [];

  const getActivityEmoji = (type: string): string => {
    const emojiMap: Record<string, string> = {
      fitness: '🏃',
      food: '🥗',
      medication: '💊',
      therapy: '🧘',
      consultation: '👨‍⚕️',
    };
    return emojiMap[type.toLowerCase()] || '📌';
  };

  const getActivityColor = (type: string): string => {
    const colorMap: Record<string, string> = {
      fitness: '#2ca02c',
      food: '#ff7f0e',
      medication: '#d62728',
      therapy: '#9467bd',
      consultation: '#1f77b4',
    };
    return colorMap[type.toLowerCase()] || '#ccc';
  };

  return (
    <div className="schedule-viewer">
      <h2>📅 Schedule Viewer</h2>
      
      <div className="date-selector">
        <label htmlFor="dateSelect">Select Date:</label>
        <select
          id="dateSelect"
          value={displayDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="date-select"
        >
          {dates.map((date) => (
            <option key={date} value={date}>
              {format(parseISO(date), 'EEEE, MMMM d, yyyy')}
            </option>
          ))}
        </select>
      </div>

      <div className="schedule-day">
        <h3>{format(parseISO(displayDate), 'EEEE, MMMM d, yyyy')}</h3>
        <p className="activity-count">{dayActivities.length} activities scheduled</p>

        {dayActivities.length === 0 ? (
          <p className="no-activities">No activities scheduled for this day.</p>
        ) : (
          <div className="activities-list">
            {dayActivities
              .sort((a, b) => a.scheduled_time.localeCompare(b.scheduled_time))
              .map((activity, index) => (
                <div
                  key={index}
                  className="activity-card"
                  style={{ borderLeftColor: getActivityColor(activity.activity_type) }}
                >
                  <div className="activity-header">
                    <span className="activity-emoji">{getActivityEmoji(activity.activity_type)}</span>
                    <div className="activity-info">
                      <h4>{activity.activity_name}</h4>
                      <div className="activity-meta">
                        <span className="time-badge">
                          {activity.scheduled_time} - {activity.end_time}
                        </span>
                        <span className="type-badge" style={{ backgroundColor: getActivityColor(activity.activity_type) }}>
                          {activity.activity_type}
                        </span>
                        {activity.is_backup && (
                          <span className="backup-badge">Backup</span>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="activity-details">
                    {activity.details && (
                      <p className="details">{activity.details}</p>
                    )}
                    <div className="activity-meta-info">
                      <span>📍 {activity.location}</span>
                      {activity.facilitator && <span>👤 {activity.facilitator}</span>}
                      <span>⏱️ {activity.duration_minutes} min</span>
                    </div>
                    {activity.notes && (
                      <p className="notes">📝 {activity.notes}</p>
                    )}
                  </div>
                </div>
              ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default ScheduleViewer;
