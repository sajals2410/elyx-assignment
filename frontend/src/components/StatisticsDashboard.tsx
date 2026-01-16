import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Statistics } from '../api';
import './StatisticsDashboard.css';

interface StatisticsDashboardProps {
  statistics: Statistics | null;
}

const StatisticsDashboard: React.FC<StatisticsDashboardProps> = ({ statistics }) => {
  if (!statistics) {
    return (
      <div className="statistics-dashboard">
        <p>No statistics available. Generate a schedule first.</p>
      </div>
    );
  }

  const typeData = Object.entries(statistics.by_type || {}).map(([type, count]) => ({
    name: type.charAt(0).toUpperCase() + type.slice(1),
    count: count,
  }));

  const priorityData = Object.entries(statistics.by_priority || {}).map(([priority, count]) => ({
    name: priority.charAt(0).toUpperCase() + priority.slice(1),
    count: count,
  }));

  const COLORS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'];

  const typeColors: Record<string, string> = {
    Fitness: '#2ca02c',
    Food: '#ff7f0e',
    Medication: '#d62728',
    Therapy: '#9467bd',
    Consultation: '#1f77b4',
  };

  return (
    <div className="statistics-dashboard">
      <h2>📊 Schedule Statistics</h2>
      
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{statistics.total_activities}</div>
          <div className="stat-label">Total Activities</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{statistics.total_days}</div>
          <div className="stat-label">Days Scheduled</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{statistics.total_hours.toFixed(1)}h</div>
          <div className="stat-label">Total Time</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{statistics.backup_activities}</div>
          <div className="stat-label">Backup Activities</div>
        </div>
      </div>

      <div className="charts-container">
        <div className="chart-card">
          <h3>Activities by Type</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={typeData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#1f77b4" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="chart-card">
          <h3>Activities by Priority</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={priorityData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${((percent || 0) * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="count"
              >
                {priorityData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="breakdown-section">
        <h3>Detailed Breakdown</h3>
        <div className="breakdown-grid">
          <div>
            <h4>By Type</h4>
            <ul>
              {typeData.map((item) => (
                <li key={item.name}>
                  <span className="type-badge" style={{ backgroundColor: typeColors[item.name] || '#ccc' }}>
                    {item.name}
                  </span>
                  <span className="count">{item.count}</span>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4>By Priority</h4>
            <ul>
              {priorityData.map((item) => (
                <li key={item.name}>
                  <span className="priority-badge">{item.name}</span>
                  <span className="count">{item.count}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatisticsDashboard;
