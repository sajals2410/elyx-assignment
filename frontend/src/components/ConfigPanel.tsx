import React, { useState } from 'react';
import './ConfigPanel.css';

interface ConfigPanelProps {
  onGenerate: (startDate: string, weeks: number, regenerateData: boolean, useGemini: boolean) => void;
  loading: boolean;
}

const ConfigPanel: React.FC<ConfigPanelProps> = ({ onGenerate, loading }) => {
  const [startDate, setStartDate] = useState('2026-01-15');
  const [weeks, setWeeks] = useState(2);
  const [regenerateData, setRegenerateData] = useState(false);
  const [useGemini, setUseGemini] = useState(true);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGenerate(startDate, weeks, regenerateData, useGemini);
  };

  return (
    <div className="config-panel">
      <h2>⚙️ Schedule Configuration</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="startDate">Start Date</label>
          <input
            type="date"
            id="startDate"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="weeks">Number of Weeks: {weeks}</label>
          <input
            type="range"
            id="weeks"
            min="1"
            max="24"
            value={weeks}
            onChange={(e) => setWeeks(Number(e.target.value))}
          />
          <div className="range-labels">
            <span>1 week</span>
            <span>24 weeks</span>
          </div>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={regenerateData}
              onChange={(e) => setRegenerateData(e.target.checked)}
            />
            Regenerate Test Data
          </label>
        </div>

        <div className="form-group checkbox-group">
          <label>
            <input
              type="checkbox"
              checked={useGemini}
              onChange={(e) => setUseGemini(e.target.checked)}
            />
            🤖 Use Gemini AI for Activity Generation
          </label>
          <small style={{display: 'block', marginTop: '0.5rem', color: '#666', fontSize: '0.85em'}}>
            Requires GEMINI_API_KEY environment variable. Falls back to templates if not set.
          </small>
        </div>

        <button type="submit" className="generate-btn" disabled={loading}>
          {loading ? '⏳ Generating...' : '🚀 Generate Schedule'}
        </button>
      </form>
    </div>
  );
};

export default ConfigPanel;
