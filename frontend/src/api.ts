/**
 * API service for communicating with the Flask backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

export interface ScheduleActivity {
  activity_id: string;
  activity_name: string;
  activity_type: string;
  scheduled_date: string;
  scheduled_time: string;
  end_time: string;
  duration_minutes: number;
  details: string;
  facilitator: string;
  location: string;
  is_remote: boolean;
  is_backup: boolean;
  original_activity_id: string | null;
  notes: string;
}

export interface Statistics {
  total_activities: number;
  total_days: number;
  total_minutes: number;
  total_hours: number;
  by_type: Record<string, number>;
  by_priority: Record<string, number>;
  backup_activities: number;
}

export interface ScheduleData {
  generated_at: string;
  statistics: Statistics;
  schedule: Record<string, ScheduleActivity[]>;
}

class ApiService {
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const data = await response.json();
      return data.status === 'ok';
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  async generateData(startDate: string, durationMonths: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/generate-data`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        start_date: startDate,
        duration_months: durationMonths,
      }),
    });
    return response.json();
  }

  async generateSchedule(startDate: string, weeks: number): Promise<any> {
    const response = await fetch(`${API_BASE_URL}/generate-schedule`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        start_date: startDate,
        weeks: weeks,
      }),
    });
    return response.json();
  }

  async getSchedule(): Promise<ScheduleData | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/schedule`);
      const data = await response.json();
      return data.success ? data.data : null;
    } catch (error) {
      console.error('Failed to get schedule:', error);
      return null;
    }
  }

  async getStatistics(): Promise<Statistics | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/statistics`);
      const data = await response.json();
      return data.success ? data.statistics : null;
    } catch (error) {
      console.error('Failed to get statistics:', error);
      return null;
    }
  }

  downloadFile(fileType: 'text' | 'html' | 'ics' | 'json'): void {
    window.open(`${API_BASE_URL}/download/${fileType}`, '_blank');
  }
}

export const apiService = new ApiService();
