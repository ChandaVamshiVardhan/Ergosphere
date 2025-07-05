"""
Serializers for the tasks app in Smart Todo.

This module contains Django REST Framework serializers that handle
conversion between Django model instances and JSON data for API responses.
"""

from rest_framework import serializers
from .models import Task, Category, DailyContext, TaskSuggestion

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    
    Handles serialization of category data including id, name, color, and creation date.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'color', 'created_at']

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    
    Includes category_name as a read-only field and handles all task-related data.
    Auto-enhances task description if AI is available during creation.
    """
    # Read-only field to include category name in responses
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'category', 'category_name', 
            'priority', 'status', 'deadline', 'estimated_duration', 
            'tags', 'ai_priority_score', 'ai_enhanced_description',
            'created_at', 'updated_at', 'completed_at'
        ]
    
    def create(self, validated_data):
        """
        Override create method to add AI enhancement capabilities.
        Currently creates the task as-is, but can be extended for AI processing.
        """
        # Auto-enhance description if AI is available
        task = super().create(validated_data)
        return task

class DailyContextSerializer(serializers.ModelSerializer):
    """
    Serializer for DailyContext model.
    
    Handles serialization of context data including content, type, timestamps,
    and AI analysis results (keywords, sentiment, urgency scores).
    """
    class Meta:
        model = DailyContext
        fields = [
            'id', 'content', 'context_type', 'timestamp', 'sender',
            'subject', 'keywords', 'sentiment_score', 'urgency_score',
            'processed'
        ]

class TaskSuggestionSerializer(serializers.ModelSerializer):
    """
    Serializer for TaskSuggestion model.
    
    Handles serialization of AI-generated task suggestions including
    suggested category, priority, deadline, and confidence scores.
    """
    class Meta:
        model = TaskSuggestion
        fields = [
            'id', 'title', 'description', 'suggested_category',
            'suggested_priority', 'suggested_deadline', 'confidence_score',
            'based_on_context', 'created_at', 'accepted'
        ]