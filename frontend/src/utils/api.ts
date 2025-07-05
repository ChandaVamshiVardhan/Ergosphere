// API utility for Smart Todo frontend
// Provides functions for interacting with backend endpoints for tasks, categories, context, AI, and suggestions

import axios from 'axios';
import { Task, Category, DailyContext, TaskSuggestion, AIAnalysis, TaskAnalytics } from '@/types';

import config from '../../config';

const API_BASE_URL = config.API_URL;

// Create a pre-configured Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Task APIs: CRUD operations for tasks
export const taskApi = {
  getAll: (params?: { status?: string; priority?: string; category?: string; search?: string }) =>
    api.get<Task[]>('/tasks/', { params }),
  
  getById: (id: number) => api.get<Task>(`/tasks/${id}/`),
  
  create: (data: Partial<Task>) => api.post<Task>('/tasks/', data),
  
  update: (id: number, data: Partial<Task>) => api.put<Task>(`/tasks/${id}/`, data),
  
  delete: (id: number) => api.delete(`/tasks/${id}/`),
};

// Category APIs: CRUD for categories
export const categoryApi = {
  getAll: () => api.get<Category[]>('/categories/'),
  
  create: (data: Partial<Category>) => api.post<Category>('/categories/', data),
};

// Daily Context APIs: CRUD for context entries
export const contextApi = {
  getAll: () => api.get<DailyContext[]>('/context/'),
  
  create: (data: Partial<DailyContext>) => api.post<DailyContext>('/context/', data),
};

// AI APIs: Suggestions and analytics
export const aiApi = {
  getSuggestions: (data: {
    task_data?: Partial<Task>;
    context_data?: Partial<DailyContext>;
    action: 'prioritize' | 'suggest_deadline' | 'categorize' | 'enhance_description' | 'generate_suggestions' | 'analyze_context';
  }) => api.post('/ai/suggestions/', data),
  
  getAnalytics: () => api.get<TaskAnalytics>('/ai/analytics/'),
};

// Task Suggestions APIs: Get and accept suggestions
export const suggestionApi = {
  getAll: (params?: { min_confidence?: number; days_back?: number }) =>
    api.get<TaskSuggestion[]>('/suggestions/', { params }),
  
  accept: (id: number) => api.post(`/suggestions/${id}/accept/`),
};

export default api; 