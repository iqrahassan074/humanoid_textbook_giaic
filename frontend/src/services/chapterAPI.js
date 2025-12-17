import axios from 'axios';

// Base API URL - this should match your backend server
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 second timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token if needed
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Chapter API functions
const chapterAPI = {
  // Get all textbook chapters
  getChapters: async () => {
    try {
      const response = await apiClient.get('/chapters');
      return response.data;
    } catch (error) {
      console.error('Error fetching chapters:', error);
      throw error;
    }
  },

  // Get a specific chapter by ID
  getChapter: async (chapterId) => {
    try {
      const response = await apiClient.get(`/chapters/${chapterId}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching chapter ${chapterId}:`, error);
      throw error;
    }
  }
};

export default chapterAPI;