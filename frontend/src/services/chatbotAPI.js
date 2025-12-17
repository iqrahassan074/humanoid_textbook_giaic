import axios from 'axios';

// Base API URL - in production, this should be configurable
const API_BASE_URL = 'http://localhost:8000';

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

// Chatbot API functions
const chatbotAPI = {
  // Ask a question to the chatbot
  askQuestion: async (question, chapterId = null) => {
    try {
      const response = await apiClient.post('/chatbot/ask', {
        question,
        chapter_id: chapterId,
        include_citations: true
      });
      return response.data;
    } catch (error) {
      console.error('Error asking question:', error);
      throw error;
    }
  },

  // Get question history for the authenticated user
  getQuestionHistory: async () => {
    try {
      const response = await apiClient.get('/chatbot/history');
      return response.data;
    } catch (error) {
      console.error('Error getting question history:', error);
      throw error;
    }
  },

  // Test the RAG pipeline
  testRagPipeline: async () => {
    try {
      const response = await apiClient.post('/chatbot/test-rag');
      return response.data;
    } catch (error) {
      console.error('Error testing RAG pipeline:', error);
      throw error;
    }
  }
};

export default chatbotAPI;