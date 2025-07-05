// TaskForm component for creating and editing tasks in Smart Todo
// Includes AI-powered suggestions for category and priority

'use client';

import { useState, useEffect } from 'react';
import { Task, Category } from '@/types';
import { taskApi, categoryApi, aiApi } from '@/utils/api';
import { 
  X, 
  Sparkles, 
  Calendar, 
  Clock, 
  Tag,
  Loader2
} from 'lucide-react';

// Props for TaskForm: task (optional), onSave, onCancel
interface TaskFormProps {
  task?: Task;
  onSave: (task: Task) => void;
  onCancel: () => void;
}

// Main TaskForm component
export default function TaskForm({ task, onSave, onCancel }: TaskFormProps) {
  // State for form fields
  const [formData, setFormData] = useState({
    title: task?.title || '',
    description: task?.description || '',
    category: task?.category || undefined,
    priority: task?.priority || 'medium',
    status: task?.status || 'pending',
    deadline: task?.deadline ? task.deadline.slice(0, 16) : '',
    estimated_duration: task?.estimated_duration || 60,
    tags: task?.tags || [],
  });

  // State for categories, loading, and AI suggestions
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [aiSuggestions, setAiSuggestions] = useState<any>(null);
  const [showAiSuggestions, setShowAiSuggestions] = useState(false);

  // Fetch categories on mount
  useEffect(() => {
    fetchCategories();
  }, []);

  // Fetch all categories from API
  const fetchCategories = async () => {
    try {
      const response = await categoryApi.getAll();
      setCategories(response.data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  // Handle input changes for form fields
  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  // Handle tags input (comma-separated)
  const handleTagsChange = (value: string) => {
    const tags = value.split(',').map(tag => tag.trim()).filter(tag => tag);
    setFormData(prev => ({ ...prev, tags }));
  };

  // Request AI suggestions for category/priority
  const getAiSuggestions = async () => {
    if (!formData.title) return;

    setLoading(true);
    try {
      const response = await aiApi.getSuggestions({
        task_data: formData,
        action: 'categorize'
      });

      if (response.data.categorization) {
        setAiSuggestions(response.data.categorization);
        setShowAiSuggestions(true);
      }
    } catch (error) {
      console.error('Failed to get AI suggestions:', error);
    } finally {
      setLoading(false);
    }
  };

  // Apply AI suggestion to form fields
  const applyAiSuggestion = (suggestion: any) => {
    if (suggestion.suggested_category) {
      setFormData(prev => ({ 
        ...prev, 
        category: parseInt(suggestion.suggested_category) || undefined
      }));
    }
    if (suggestion.suggested_priority) {
      setFormData(prev => ({ 
        ...prev, 
        priority: suggestion.suggested_priority 
      }));
    }
    setShowAiSuggestions(false);
  };

  // Handle form submission for create/update
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      let savedTask: Task;
      
      if (task) {
        // Update existing task
        const response = await taskApi.update(task.id, formData);
        savedTask = response.data;
      } else {
        // Create new task
        const response = await taskApi.create(formData);
        savedTask = response.data;
      }

      onSave(savedTask);
    } catch (error) {
      console.error('Failed to save task:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    // Modal overlay for the form
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div className="p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">
              {task ? 'Edit Task' : 'Create New Task'}
            </h2>
            <button
              onClick={onCancel}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Title input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Title *
              </label>
              <input
                type="text"
                value={formData.title}
                onChange={(e) => handleInputChange('title', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>

            {/* Description input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                value={formData.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* AI Suggestions Button */}
            {formData.title && (
              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={getAiSuggestions}
                  disabled={loading}
                  className="flex items-center gap-2 px-4 py-2 bg-purple-100 text-purple-700 rounded-md hover:bg-purple-200 disabled:opacity-50"
                >
                  {loading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Sparkles className="w-4 h-4" />
                  )}
                  Get AI Suggestions
                </button>
              </div>
            )}

            {/* AI Suggestions */}
            {showAiSuggestions && aiSuggestions && (
              <div className="bg-blue-50 p-4 rounded-md">
                <h3 className="text-sm font-medium text-blue-900 mb-2">AI Suggestions</h3>
                <div className="space-y-2">
                  {aiSuggestions.suggested_category && (
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-800">Category:</span>
                      <button
                        type="button"
                        onClick={() => applyAiSuggestion(aiSuggestions)}
                        className="text-sm text-blue-600 hover:text-blue-800 underline"
                      >
                        {aiSuggestions.suggested_category} (Confidence: {Math.round(aiSuggestions.confidence * 100)}%)
                      </button>
                    </div>
                  )}
                  {/* Add more AI suggestion fields as needed */}
                </div>
              </div>
            )}

            {/* Category and Priority */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  value={formData.category || ''}
                  onChange={(e) => handleInputChange('category', e.target.value ? parseInt(e.target.value) : undefined)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">Select Category</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Priority
                </label>
                <select
                  value={formData.priority}
                  onChange={(e) => handleInputChange('priority', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
              </div>
            </div>

            {/* Deadline and Duration */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Deadline
                </label>
                <input
                  type="datetime-local"
                  value={formData.deadline}
                  onChange={(e) => handleInputChange('deadline', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Estimated Duration (minutes)
                </label>
                <input
                  type="number"
                  value={formData.estimated_duration}
                  onChange={(e) => handleInputChange('estimated_duration', parseInt(e.target.value) || 0)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Tags */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tags (comma-separated)
              </label>
              <input
                type="text"
                value={formData.tags.join(', ')}
                onChange={(e) => handleTagsChange(e.target.value)}
                placeholder="work, urgent, project"
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Status */}
            {task && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Status
                </label>
                <select
                  value={formData.status}
                  onChange={(e) => handleInputChange('status', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center justify-end gap-3 pt-6 border-t border-gray-200">
              <button
                type="button"
                onClick={onCancel}
                className="px-4 py-2 text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    Saving...
                  </div>
                ) : (
                  task ? 'Update Task' : 'Create Task'
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
} 