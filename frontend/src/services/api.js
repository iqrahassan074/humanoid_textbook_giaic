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

// Request interceptor to add auth token
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

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token might be expired, redirect to login
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API service functions
const apiService = {
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
      console.error('Error fetching chapter:', error);
      throw error;
    }
  },

  // Get current user info
  getCurrentUser: async () => {
    try {
      const response = await apiClient.get('/auth/me');
      return response.data;
    } catch (error) {
      console.error('Error fetching user info:', error);
      throw error;
    }
  },

  // Logout user
  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
      // Token removal handled by interceptor
    } catch (error) {
      console.error('Error during logout:', error);
      // Still remove token locally even if backend request fails
      localStorage.removeItem('token');
    }
  }
};

export default apiService;