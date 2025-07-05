"""
URL configuration for the tasks app in Smart Todo.

Defines all API endpoints for tasks, categories, daily context, AI features,
and task suggestions. All URLs are prefixed with 'api/' from the main urls.py.
"""

from django.urls import path
from . import views

# URL patterns for the tasks app
urlpatterns = [
    # Task endpoints - CRUD operations for tasks
    path('tasks/', views.TaskListCreateView.as_view(), name='task-list-create'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task-detail'),
    
    # Category endpoints - CRUD operations for categories
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    
    # Daily context endpoints - CRUD operations for context entries
    path('context/', views.DailyContextListCreateView.as_view(), name='context-list-create'),
    
    # AI-powered endpoints - AI suggestions and analytics
    path('ai/suggestions/', views.get_ai_task_suggestions, name='ai-suggestions'),
    path('ai/analytics/', views.get_task_analytics, name='task-analytics'),
    
    # Task suggestions endpoints - Get and accept AI suggestions
    path('suggestions/', views.TaskSuggestionListView.as_view(), name='task-suggestions'),
    path('suggestions/<int:suggestion_id>/accept/', views.accept_task_suggestion, name='accept-suggestion'),
]