// useTasks custom React hook for Smart Todo
// Manages fetching, creating, updating, deleting, and filtering tasks from the API

import { useState, useEffect, useCallback } from 'react';
import { Task } from '@/types';
import { taskApi } from '@/utils/api';

export const useTasks = () => {
  // State for tasks, loading, error, and filters
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState({
    status: '',
    priority: '',
    category: '',
    search: '',
  });

  // Fetch tasks from API with current filters
  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await taskApi.getAll(filters);
      setTasks(response.data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  }, [filters]);

  // Create a new task
  const createTask = useCallback(async (taskData: Partial<Task>) => {
    try {
      const response = await taskApi.create(taskData);
      setTasks(prev => [response.data, ...prev]);
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create task');
      throw err;
    }
  }, []);

  // Update an existing task
  const updateTask = useCallback(async (id: number, taskData: Partial<Task>) => {
    try {
      const response = await taskApi.update(id, taskData);
      setTasks(prev => prev.map(task => task.id === id ? response.data : task));
      return response.data;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update task');
      throw err;
    }
  }, []);

  // Delete a task
  const deleteTask = useCallback(async (id: number) => {
    try {
      await taskApi.delete(id);
      setTasks(prev => prev.filter(task => task.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete task');
      throw err;
    }
  }, []);

  // Update filters for task fetching
  const updateFilters = useCallback((newFilters: Partial<typeof filters>) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  }, []);

  // Fetch tasks on mount and when filters change
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Return state and actions for use in components
  return {
    tasks,
    loading,
    error,
    filters,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    updateFilters,
  };
}; 