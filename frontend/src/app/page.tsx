// Dashboard page for Smart Todo
// Provides the main UI for managing, filtering, and viewing tasks with AI-powered features

'use client';

import { useState } from 'react';
import { useTasks } from '@/hooks/useTasks';
import TaskCard from '@/components/TaskCard';
import TaskForm from '@/components/TaskForm';
import { Task } from '@/types';
import { 
  Plus, 
  Search, 
  Filter, 
  Sparkles, 
  BarChart3,
  MessageSquare,
  Calendar,
  CheckCircle
} from 'lucide-react';

export default function Dashboard() {
  // Custom hook to manage tasks and related actions
  const {
    tasks,
    loading,
    error,
    filters,
    createTask,
    updateTask,
    deleteTask,
    updateFilters,
  } = useTasks();

  // Local state for UI controls
  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [activeTab, setActiveTab] = useState<'tasks' | 'context' | 'analytics'>('tasks');

  // Handlers for task creation/editing
  const handleCreateTask = () => {
    setEditingTask(null);
    setShowTaskForm(true);
  };

  const handleEditTask = (task: Task) => {
    setEditingTask(task);
    setShowTaskForm(true);
  };

  const handleSaveTask = (task: Task) => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  const handleCancelTask = () => {
    setShowTaskForm(false);
    setEditingTask(null);
  };

  // Handler for deleting a task
  const handleDeleteTask = async (id: number) => {
    if (confirm('Are you sure you want to delete this task?')) {
      await deleteTask(id);
    }
  };

  // Handler for changing task status
  const handleStatusChange = async (id: number, status: Task['status']) => {
    await updateTask(id, { status });
  };

  // Filter tasks based on current filters
  const getFilteredTasks = () => {
    return tasks.filter(task => {
      if (filters.status && task.status !== filters.status) return false;
      if (filters.priority && task.priority !== filters.priority) return false;
      if (filters.category && task.category_name !== filters.category) return false;
      if (filters.search) {
        const searchLower = filters.search.toLowerCase();
        return (
          task.title.toLowerCase().includes(searchLower) ||
          task.description.toLowerCase().includes(searchLower) ||
          task.tags.some(tag => tag.toLowerCase().includes(searchLower))
        );
      }
      return true;
    });
  };

  const filteredTasks = getFilteredTasks();

  // Compute statistics for the stats bar
  const getTaskStats = () => {
    const total = tasks.length;
    const completed = tasks.filter(t => t.status === 'completed').length;
    const pending = tasks.filter(t => t.status === 'pending').length;
    const urgent = tasks.filter(t => t.priority === 'urgent').length;
    
    return { total, completed, pending, urgent };
  };

  const stats = getTaskStats();

  // Show loading spinner if tasks are loading
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header: App title and New Task button */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Smart Todo</h1>
              <div className="ml-4 flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-purple-600" />
                <span className="text-sm text-gray-600">AI-Powered</span>
              </div>
            </div>
            
            <button
              onClick={handleCreateTask}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors"
            >
              <Plus className="w-4 h-4" />
              New Task
            </button>
          </div>
        </div>
      </header>

      {/* Stats Bar: Shows total, completed, pending, urgent tasks */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">{stats.total}</div>
              <div className="text-sm text-gray-600">Total Tasks</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.completed}</div>
              <div className="text-sm text-gray-600">Completed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
              <div className="text-sm text-gray-600">Pending</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-red-600">{stats.urgent}</div>
              <div className="text-sm text-gray-600">Urgent</div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs: Switch between Tasks, Context, Analytics */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('tasks')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'tasks'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4" />
                Tasks
              </div>
            </button>
            <button
              onClick={() => setActiveTab('context')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'context'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center gap-2">
                <MessageSquare className="w-4 h-4" />
                Daily Context
              </div>
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'analytics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center gap-2">
                <BarChart3 className="w-4 h-4" />
                Analytics
              </div>
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'tasks' && (
          <div className="space-y-6">
            {/* Filters */}
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center gap-4 flex-wrap">
                <div className="flex-1 min-w-64">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-4 h-4" />
                    <input
                      type="text"
                      placeholder="Search tasks..."
                      value={filters.search}
                      onChange={(e) => updateFilters({ search: e.target.value })}
                      className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                </div>
                
                <select
                  value={filters.status}
                  onChange={(e) => updateFilters({ status: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Status</option>
                  <option value="pending">Pending</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                  <option value="cancelled">Cancelled</option>
                </select>
                
                <select
                  value={filters.priority}
                  onChange={(e) => updateFilters({ priority: e.target.value })}
                  className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="">All Priorities</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="urgent">Urgent</option>
                </select>
                
                <button
                  onClick={() => updateFilters({ status: '', priority: '', category: '', search: '' })}
                  className="px-3 py-2 text-gray-600 hover:text-gray-800"
                >
                  Clear
                </button>
              </div>
            </div>

            {/* Task List */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-md p-4">
                <p className="text-red-800">{error}</p>
              </div>
            )}

            {filteredTasks.length === 0 ? (
              <div className="text-center py-12">
                <CheckCircle className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">No tasks found</h3>
                <p className="text-gray-600 mb-4">
                  {filters.search || filters.status || filters.priority
                    ? 'Try adjusting your filters'
                    : 'Get started by creating your first task'}
                </p>
                {!filters.search && !filters.status && !filters.priority && (
                  <button
                    onClick={handleCreateTask}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                  >
                    <Plus className="w-4 h-4" />
                    Create Task
                  </button>
                )}
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {filteredTasks.map((task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onEdit={handleEditTask}
                    onDelete={handleDeleteTask}
                    onStatusChange={handleStatusChange}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'context' && (
          <div className="text-center py-12">
            <MessageSquare className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Daily Context</h3>
            <p className="text-gray-600">Add your daily context (messages, emails, notes) for AI-powered task suggestions.</p>
            <p className="text-sm text-gray-500 mt-2">Coming soon...</p>
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="text-center py-12">
            <BarChart3 className="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">Analytics & Insights</h3>
            <p className="text-gray-600">View detailed analytics and AI insights about your task management.</p>
            <p className="text-sm text-gray-500 mt-2">Coming soon...</p>
          </div>
        )}
      </main>

      {/* Task Form Modal */}
      {showTaskForm && (
        <TaskForm
          task={editingTask || undefined}
          onSave={handleSaveTask}
          onCancel={handleCancelTask}
        />
      )}
    </div>
  );
}
