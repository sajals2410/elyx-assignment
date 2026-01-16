import React from 'react';
import { apiService } from '../api';
import './DownloadPanel.css';

const DownloadPanel: React.FC = () => {
  const handleDownload = (fileType: 'text' | 'html' | 'ics' | 'json') => {
    apiService.downloadFile(fileType);
  };

  return (
    <div className="download-panel">
      <h2>💾 Download Outputs</h2>
      <p className="download-description">
        Download your schedule in various formats for viewing, importing, or sharing.
      </p>
      
      <div className="download-buttons">
        <button
          className="download-btn"
          onClick={() => handleDownload('text')}
        >
          <span className="download-icon">📄</span>
          <div>
            <div className="download-title">Text Calendar</div>
            <div className="download-subtitle">.txt format</div>
          </div>
        </button>

        <button
          className="download-btn"
          onClick={() => handleDownload('html')}
        >
          <span className="download-icon">🌐</span>
          <div>
            <div className="download-title">HTML Calendar</div>
            <div className="download-subtitle">.html format</div>
          </div>
        </button>

        <button
          className="download-btn"
          onClick={() => handleDownload('ics')}
        >
          <span className="download-icon">📅</span>
          <div>
            <div className="download-title">iCalendar</div>
            <div className="download-subtitle">Import to calendar apps</div>
          </div>
        </button>

        <button
          className="download-btn"
          onClick={() => handleDownload('json')}
        >
          <span className="download-icon">📊</span>
          <div>
            <div className="download-title">JSON Summary</div>
            <div className="download-subtitle">.json format</div>
          </div>
        </button>
      </div>
    </div>
  );
};

export default DownloadPanel;
