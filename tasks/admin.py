"""
Django admin configuration for the tasks app in Smart Todo.

This module configures the Django admin interface for all models,
providing a user-friendly way to manage tasks, categories, context, and suggestions.
"""

from django.contrib import admin
from .models import Task, Category, DailyContext, TaskSuggestion

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    
    Provides a simple interface for managing task categories with search functionality.
    """
    list_display = ['name', 'color', 'created_at']  # Fields to display in list view
    search_fields = ['name']  # Enable search by category name

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin configuration for Task model.
    
    Provides comprehensive task management with filtering, search, and organized fieldsets.
    Includes AI-enhanced fields as read-only for monitoring.
    """
    list_display = ['title', 'category', 'priority', 'status', 'deadline', 'ai_priority_score', 'created_at']
    list_filter = ['status', 'priority', 'category', 'created_at']  # Filter options in sidebar
    search_fields = ['title', 'description']  # Search functionality
    readonly_fields = ['ai_priority_score', 'ai_enhanced_description', 'completed_at']  # Read-only AI fields
    
    # Organize fields into logical groups
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'tags')
        }),
        ('Task Details', {
            'fields': ('priority', 'status', 'deadline', 'estimated_duration')
        }),
        ('AI Enhancements', {
            'fields': ('ai_priority_score', 'ai_enhanced_description'),
            'classes': ('collapse',)  # Collapsible section
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)  # Collapsible section
        })
    )

@admin.register(DailyContext)
class DailyContextAdmin(admin.ModelAdmin):
    """
    Admin configuration for DailyContext model.
    
    Provides interface for managing daily context entries with AI analysis results.
    AI-generated fields are read-only to prevent manual modification.
    """
    list_display = ['context_type', 'sender', 'subject', 'timestamp', 'urgency_score', 'processed']
    list_filter = ['context_type', 'processed', 'timestamp']  # Filter by context type and processing status
    search_fields = ['content', 'sender', 'subject']  # Search in content and metadata
    readonly_fields = ['sentiment_score', 'urgency_score', 'keywords']  # AI analysis results are read-only

@admin.register(TaskSuggestion)
class TaskSuggestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for TaskSuggestion model.
    
    Provides interface for managing AI-generated task suggestions.
    Useful for monitoring suggestion quality and acceptance rates.
    """
    list_display = ['title', 'suggested_category', 'suggested_priority', 'confidence_score', 'accepted', 'created_at']
    list_filter = ['accepted', 'suggested_priority', 'created_at']  # Filter by acceptance and priority
    search_fields = ['title', 'description']  # Search in suggestion content
