"""
Utility functions and classes for the tasks app in Smart Todo.

This module provides enhanced task analysis utilities including time extraction,
workload calculation, and optimal scheduling suggestions.
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any

class TaskAnalyzer:
    """
    Enhanced task analysis utilities.
    
    Provides methods for analyzing task content, extracting time mentions,
    calculating workload scores, and suggesting optimal schedules.
    """
    
    def __init__(self):
        """
        Initialize the TaskAnalyzer with priority keywords for analysis.
        """
        # Keywords that indicate different priority levels
        self.priority_keywords = {
            'urgent': ['urgent', 'asap', 'immediately', 'critical', 'emergency'],
            'high': ['important', 'priority', 'deadline', 'soon', 'quick'],
            'medium': ['normal', 'regular', 'standard', 'moderate'],
            'low': ['later', 'whenever', 'optional', 'nice-to-have']
        }
    
    def extract_time_mentions(self, text: str) -> List[str]:
        """
        Extract time-related mentions from text using regex patterns.
        
        Args:
            text: The text to analyze for time mentions
            
        Returns:
            List of time-related strings found in the text
        """
        # Regex patterns for different time formats
        time_patterns = [
            r'(\d{1,2}:\d{2}(?:\s?(?:AM|PM))?)',  # Time format (e.g., "2:30 PM")
            r'(tomorrow|today|yesterday)',  # Relative days
            r'(next week|this week|last week)',  # Relative weeks
            r'(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',  # Days of week
            r'(\d{1,2}(?:st|nd|rd|th)?\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec))',  # Dates
        ]
        
        time_mentions = []
        for pattern in time_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            time_mentions.extend(matches)
        
        return time_mentions
    
    def calculate_workload_score(self, tasks: List[Any]) -> float:
        """
        Calculate current workload score based on pending and high-priority tasks.
        
        Args:
            tasks: List of task objects to analyze
            
        Returns:
            Workload score between 0.0 and 1.0
        """
        if not tasks:
            return 0.0
        
        # Filter tasks by status and priority
        pending_tasks = [t for t in tasks if t.status == 'pending']
        high_priority_tasks = [t for t in pending_tasks if t.priority in ['high', 'urgent']]
        
        # Calculate workload score (weighted by task count and priority)
        workload_score = len(pending_tasks) * 0.1 + len(high_priority_tasks) * 0.2
        return min(workload_score, 1.0)  # Cap at 1.0
    
    def suggest_optimal_schedule(self, tasks: List[Any]) -> Dict[str, Any]:
        """
        Suggest optimal task scheduling based on priority and estimated duration.
        
        Args:
            tasks: List of task objects to schedule
            
        Returns:
            Dictionary containing suggested schedule and reasoning
        """
        if not tasks:
            return {'schedule': [], 'reasoning': 'No tasks to schedule'}
        
        # Sort tasks by AI priority score and deadline
        sorted_tasks = sorted(
            tasks, 
            key=lambda t: (t.ai_priority_score, t.deadline or datetime.max),
            reverse=True
        )
        
        schedule = []
        current_time = datetime.now()
        
        # Schedule top 10 tasks with estimated durations
        for task in sorted_tasks[:10]:
            estimated_end = current_time + timedelta(
                minutes=task.estimated_duration or 60  # Default to 60 minutes
            )
            
            schedule.append({
                'task_id': task.id,
                'title': task.title,
                'suggested_start': current_time.isoformat(),
                'suggested_end': estimated_end.isoformat(),
                'priority_score': task.ai_priority_score
            })
            
            # Add 15-minute break between tasks
            current_time = estimated_end + timedelta(minutes=15)
        
        return {
            'schedule': schedule,
            'reasoning': f'Scheduled {len(schedule)} tasks based on priority and estimated duration'
        }