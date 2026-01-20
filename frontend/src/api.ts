/**
 * API service for communicating with the Flask backend
 */

// API URL configuration
// Set REACT_APP_API_URL in Vercel environment variables for production
// Or update this directly for Railway backend
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://your-api.railway.app/api'  // Update with your Railway URL
    : 'http://localhost:5001/api');

// Log API URL for debugging (only in development)
if (process.env.NODE_ENV === 'development') {
  console.log('API Base URL:', API_BASE_URL);
  console.log('REACT_APP_API_URL:', process.env.REACT_APP_API_URL);
}

// Helper function to add timeout to fetch requests
function fetchWithTimeout(url: string, options: RequestInit = {}, timeout: number = 5000): Promise<Response> {
  return Promise.race([
    fetch(url, options),
    new Promise<Response>((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeout)
    )
  ]) as Promise<Response>;
}

// Check if API URL is the placeholder (should not be used)
const isPlaceholderUrl = API_BASE_URL.includes('your-api.railway.app');

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
    // Skip health check if URL is placeholder
    if (isPlaceholderUrl) {
      console.warn('API URL is placeholder. Set REACT_APP_API_URL environment variable in Vercel.');
      return false;
    }

    try {
      console.log('Health check: Connecting to', `${API_BASE_URL}/health`);
      const response = await fetchWithTimeout(`${API_BASE_URL}/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        mode: 'cors',
      }, 5000); // 5 second timeout
      
      console.log('Health check response status:', response.status);
      if (!response.ok) {
        const text = await response.text();
        console.error('Health check failed:', response.status, response.statusText, text);
        return false;
      }
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Expected JSON but got:', contentType, text.substring(0, 100));
        return false;
      }
      const data = await response.json();
      console.log('Health check data:', data);
      return data.status === 'ok';
    } catch (error: any) {
      if (error.message === 'Request timeout') {
        console.error('Health check timed out after 5 seconds');
      } else {
        console.error('Health check failed:', error.message, error);
      }
      return false;
    }
  }

  async generateData(startDate: string, durationMonths: number, useGemini: boolean = true): Promise<any> {
    if (isPlaceholderUrl) {
      throw new Error('API URL is not configured. Please set REACT_APP_API_URL in Vercel environment variables.');
    }

    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/generate-data`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          start_date: startDate,
          duration_months: durationMonths,
          use_gemini: useGemini,
        }),
      }, 30000); // 30 second timeout for data generation
      
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`API error: ${response.status} - ${text.substring(0, 100)}`);
      }
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${text.substring(0, 100)}`);
      }
      return response.json();
    } catch (error: any) {
      if (error.message === 'Request timeout') {
        throw new Error('Request timed out. The backend may be slow or unreachable.');
      }
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        throw new Error(`Cannot connect to backend at ${API_BASE_URL}. Make sure the backend is running and the API URL is correct.`);
      }
      throw error;
    }
  }

  async generateSchedule(startDate: string, weeks: number): Promise<any> {
    if (isPlaceholderUrl) {
      throw new Error('API URL is not configured. Please set REACT_APP_API_URL in Vercel environment variables.');
    }

    try {
      const response = await fetchWithTimeout(`${API_BASE_URL}/generate-schedule`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          start_date: startDate,
          weeks: weeks,
        }),
      }, 30000); // 30 second timeout for schedule generation
      
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`API error: ${response.status} - ${text.substring(0, 100)}`);
      }
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        throw new Error(`Expected JSON but got: ${text.substring(0, 100)}`);
      }
      return response.json();
    } catch (error: any) {
      if (error.message === 'Request timeout') {
        throw new Error('Request timed out. The backend may be slow or unreachable.');
      }
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        throw new Error(`Cannot connect to backend at ${API_BASE_URL}. Make sure the backend is running and the API URL is correct.`);
      }
      throw error;
    }
  }

  async getSchedule(): Promise<ScheduleData | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/schedule`);
      if (!response.ok) {
        console.error('Failed to get schedule:', response.status, response.statusText);
        return null;
      }
      const data = await response.json();
      return data.success ? data.data : null;
    } catch (error: any) {
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        console.error(`Cannot connect to backend at ${API_BASE_URL}. Make sure the backend is running.`);
      } else {
        console.error('Failed to get schedule:', error);
      }
      return null;
    }
  }

  async getStatistics(): Promise<Statistics | null> {
    try {
      const response = await fetch(`${API_BASE_URL}/statistics`);
      if (!response.ok) {
        console.error('Failed to get statistics:', response.status, response.statusText);
        return null;
      }
      const data = await response.json();
      return data.success ? data.statistics : null;
    } catch (error: any) {
      if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
        console.error(`Cannot connect to backend at ${API_BASE_URL}. Make sure the backend is running.`);
      } else {
        console.error('Failed to get statistics:', error);
      }
      return null;
    }
  }

  async downloadFile(fileType: 'text' | 'html' | 'ics' | 'json'): Promise<void> {
    try {
      const response = await fetch(`${API_BASE_URL}/download/${fileType}`);
      const data = await response.json();
      
      if (data.success && data.content) {
        // Decode base64 content
        const binaryString = atob(data.content);
        const bytes = new Uint8Array(binaryString.length);
        for (let i = 0; i < binaryString.length; i++) {
          bytes[i] = binaryString.charCodeAt(i);
        }
        
        // Create blob and download
        const blob = new Blob([bytes], { type: data.contentType });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
      } else {
        console.error('Download failed:', data.error);
      }
    } catch (error) {
      console.error('Download error:', error);
    }
  }
}

export const apiService = new ApiService();
