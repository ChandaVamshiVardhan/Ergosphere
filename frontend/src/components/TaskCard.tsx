// TaskCard component for displaying a single task in Smart Todo
// Shows task details, priority, status, tags, deadline, and actions (edit, delete, complete)

'use client';

import { useState } from 'react';
import { Task } from '@/types';
import { format } from 'date-fns';
import { 
  CheckCircle, 
  Clock, 
  AlertCircle, 
  Edit, 
  Trash2, 
  Star,
  Calendar,
  Tag
} from 'lucide-react';

// Props for TaskCard: task, onEdit, onDelete, onStatusChange
interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (id: number) => void;
  onStatusChange: (id: number, status: Task['status']) => void;
}

// Color mappings for priority and status badges
const priorityColors = {
  low: 'bg-green-100 text-green-800 border-green-200',
  medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  high: 'bg-orange-100 text-orange-800 border-orange-200',
  urgent: 'bg-red-100 text-red-800 border-red-200',
};

const statusColors = {
  pending: 'bg-gray-100 text-gray-800',
  in_progress: 'bg-blue-100 text-blue-800',
  completed: 'bg-green-100 text-green-800',
  cancelled: 'bg-red-100 text-red-800',
};

// Main TaskCard component
export default function TaskCard({ task, onEdit, onDelete, onStatusChange }: TaskCardProps) {
  // State for expanding/collapsing the card
  const [isExpanded, setIsExpanded] = useState(false);

  // Get icon for task priority
  const getPriorityIcon = (priority: Task['priority']) => {
    switch (priority) {
      case 'urgent':
        return <AlertCircle className="w-4 h-4" />;
      case 'high':
        return <Star className="w-4 h-4" />;
      default:
        return <Clock className="w-4 h-4" />;
    }
  };

  // Format deadline string for display
  const formatDeadline = (deadline: string) => {
    try {
      return format(new Date(deadline), 'MMM dd, yyyy HH:mm');
    } catch {
      return 'Invalid date';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="p-4">
        {/* Header: Title, badges, and AI priority score */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-1">
              {task.title}
            </h3>
            <div className="flex items-center gap-2 flex-wrap">
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border ${priorityColors[task.priority]}`}>
                {getPriorityIcon(task.priority)}
                <span className="ml-1 capitalize">{task.priority}</span>
              </span>
              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${statusColors[task.status]}`}>
                {task.status.replace('_', ' ')}
              </span>
              {task.category_name && (
                <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                  <Tag className="w-3 h-3 mr-1" />
                  {task.category_name}
                </span>
              )}
            </div>
          </div>
          
          {/* AI Priority Score (if available) */}
          {task.ai_priority_score > 0 && (
            <div className="flex items-center gap-1 text-sm text-gray-600">
              <Star className="w-4 h-4 text-yellow-500" />
              <span>{Math.round(task.ai_priority_score * 100)}%</span>
            </div>
          )}
        </div>

        {/* Description (truncated) */}
        {task.description && (
          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
            {task.description}
          </p>
        )}

        {/* Enhanced Description (AI) */}
        {task.ai_enhanced_description && isExpanded && (
          <div className="bg-blue-50 p-3 rounded-md mb-3">
            <h4 className="text-sm font-medium text-blue-900 mb-1">AI Enhanced Description:</h4>
            <p className="text-sm text-blue-800">{task.ai_enhanced_description}</p>
          </div>
        )}

        {/* Tags */}
        {task.tags && task.tags.length > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {task.tags.map((tag, index) => (
              <span
                key={index}
                className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-700"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* Deadline */}
        {task.deadline && (
          <div className="flex items-center gap-2 text-sm text-gray-600 mb-3">
            <Calendar className="w-4 h-4" />
            <span>Due: {formatDeadline(task.deadline)}</span>
          </div>
        )}

        {/* Actions: Complete, expand, edit, delete */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-100">
          <div className="flex items-center gap-2">
            <button
              onClick={() => onStatusChange(task.id, 'completed')}
              disabled={task.status === 'completed'}
              className="flex items-center gap-1 px-3 py-1 text-sm font-medium text-green-700 bg-green-100 rounded-md hover:bg-green-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <CheckCircle className="w-4 h-4" />
              Complete
            </button>
            
            <button
              onClick={() => setIsExpanded(!isExpanded)}
              className="text-sm text-gray-600 hover:text-gray-800"
            >
              {isExpanded ? 'Show less' : 'Show more'}
            </button>
          </div>
          
          <div className="flex items-center gap-1">
            <button
              onClick={() => onEdit(task)}
              className="p-1 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded"
            >
              <Edit className="w-4 h-4" />
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="p-1 text-gray-600 hover:text-red-600 hover:bg-red-50 rounded"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
} 