"""
Views for the tasks app in Smart Todo.

This module contains all the API views for tasks, categories, daily context,
AI suggestions, and analytics. It provides RESTful endpoints for the frontend.
"""

from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from django.db import models
from datetime import datetime, timedelta
from .models import Task, Category, DailyContext, TaskSuggestion
from .serializers import TaskSerializer, CategorySerializer, DailyContextSerializer, TaskSuggestionSerializer

class TaskListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating tasks.
    
    GET: Returns a list of tasks with optional filtering
    POST: Creates a new task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        """
        Filter tasks based on query parameters.
        Supports filtering by status, priority, category, and search terms.
        """
        queryset = Task.objects.all()
        
        # Filter by status (pending, completed, etc.)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority (low, medium, high, urgent)
        priority_filter = self.request.query_params.get('priority')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        # Filter by category name
        category_filter = self.request.query_params.get('category')
        if category_filter:
            queryset = queryset.filter(category__name=category_filter)
        
        # Search functionality across title, description, and tags
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(description__icontains=search) |
                Q(tags__icontains=search)
            )
        
        # Order by AI priority score (descending) and creation date
        return queryset.order_by('-ai_priority_score', '-created_at')

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting individual tasks.
    
    GET: Returns a single task
    PUT: Updates a task
    DELETE: Deletes a task
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class CategoryListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating categories.
    
    GET: Returns a list of all categories
    POST: Creates a new category
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DailyContextListCreateView(generics.ListCreateAPIView):
    """
    API view for listing and creating daily context entries.
    
    GET: Returns a list of context entries
    POST: Creates a new context entry and processes it with AI
    """
    queryset = DailyContext.objects.all()
    serializer_class = DailyContextSerializer
    
    def perform_create(self, serializer):
        """
        Override to process context with AI after creation.
        Extracts keywords, sentiment, urgency, and generates task suggestions.
        """
        # Save the context entry
        context_instance = serializer.save()
        
        # Process with AI for analysis
        from ai_module.task_ai import task_ai
        analysis = task_ai.analyze_context({
            'content': context_instance.content,
            'context_type': context_instance.context_type,
            'id': context_instance.id
        })
        
        # Update context with AI analysis results
        context_instance.keywords = analysis['keywords']
        context_instance.sentiment_score = analysis['sentiment_score']
        context_instance.urgency_score = analysis['urgency_score']
        context_instance.processed = True
        context_instance.save()
        
        # Generate task suggestions based on context
        suggestions = task_ai.generate_task_suggestions({
            'content': context_instance.content,
            'context_type': context_instance.context_type,
            'id': context_instance.id
        })
        
        # Save generated suggestions to database
        for suggestion in suggestions:
            TaskSuggestion.objects.create(
                title=suggestion['title'],
                description=suggestion['description'],
                suggested_category=suggestion['suggested_category'],
                suggested_priority=suggestion['suggested_priority'],
                confidence_score=suggestion['confidence_score'],
                based_on_context=context_instance
            )

@api_view(['POST'])
def get_ai_task_suggestions(request):
    """
    AI-powered endpoint for task suggestions and prioritization.
    
    Supports multiple actions:
    - prioritize: Re-prioritize existing tasks
    - suggest_deadline: Suggest deadline for a task
    - categorize: Suggest category for a task
    - enhance_description: Enhance task description
    - generate_suggestions: Generate new task suggestions
    - analyze_context: Analyze context data
    """
    try:
        from ai_module.task_ai import task_ai
        
        # Extract request data
        task_data = request.data.get('task_data', {})
        context_data = request.data.get('context_data', {})
        action = request.data.get('action', 'prioritize')
        
        response_data = {}
        
        # Handle different AI actions
        if action == 'prioritize':
            # Get all pending tasks and prioritize them
            tasks = Task.objects.filter(status='pending')
            prioritized_tasks = task_ai.prioritize_tasks(tasks, context_data)
            response_data['prioritized_tasks'] = prioritized_tasks
            
        elif action == 'suggest_deadline':
            # Suggest deadline for a task
            deadline_suggestion = task_ai.suggest_deadline(task_data, context_data)
            response_data['deadline_suggestion'] = deadline_suggestion
            
        elif action == 'categorize':
            # Suggest category for a task
            categories = Category.objects.all()
            existing_categories = [cat.name for cat in categories]
            categorization = task_ai.categorize_task(task_data, existing_categories)
            response_data['categorization'] = categorization
            
        elif action == 'enhance_description':
            # Enhance task description with AI
            enhancement = task_ai.enhance_task_description(task_data, context_data)
            response_data['enhancement'] = enhancement
            
        elif action == 'generate_suggestions':
            # Generate new task suggestions from context
            suggestions = task_ai.generate_task_suggestions(context_data)
            response_data['suggestions'] = suggestions
            
        elif action == 'analyze_context':
            # Analyze context data
            analysis = task_ai.analyze_context(context_data)
            response_data['analysis'] = analysis
            
        else:
            return Response(
                {'error': 'Invalid action specified'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def get_task_analytics(request):
    """
    Analytics endpoint for task insights and statistics.
    
    Returns:
    - Summary statistics (total, completed, pending, overdue tasks)
    - Priority and category distributions
    - Recent tasks
    - AI insights (average priority scores, high priority tasks)
    """
    try:
        # Calculate basic analytics
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='completed').count()
        pending_tasks = Task.objects.filter(status='pending').count()
        overdue_tasks = Task.objects.filter(
            deadline__lt=datetime.now(),
            status='pending'
        ).count()
        
        # Calculate priority distribution
        priority_distribution = {}
        for priority, _ in Task.PRIORITY_CHOICES:
            priority_distribution[priority] = Task.objects.filter(priority=priority).count()
        
        # Calculate category distribution
        category_distribution = {}
        for category in Category.objects.all():
            category_distribution[category.name] = Task.objects.filter(category=category).count()
        
        # Get recent tasks
        recent_tasks = Task.objects.order_by('-created_at')[:5]
        recent_tasks_data = TaskSerializer(recent_tasks, many=True).data
        
        # Calculate completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Compile analytics data
        analytics_data = {
            'summary': {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'pending_tasks': pending_tasks,
                'overdue_tasks': overdue_tasks,
                'completion_rate': round(completion_rate, 2)
            },
            'priority_distribution': priority_distribution,
            'category_distribution': category_distribution,
            'recent_tasks': recent_tasks_data,
            'ai_insights': {
                'avg_priority_score': Task.objects.aggregate(
                    avg_score=models.Avg('ai_priority_score')
                )['avg_score'] or 0,
                'high_priority_tasks': Task.objects.filter(
                    ai_priority_score__gte=0.8
                ).count()
            }
        }
        
        return Response(analytics_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

class TaskSuggestionListView(generics.ListAPIView):
    """
    API view for listing task suggestions generated by AI.
    
    GET: Returns a list of unaccepted task suggestions
    """
    queryset = TaskSuggestion.objects.filter(accepted=False)
    serializer_class = TaskSuggestionSerializer
    
    def get_queryset(self):
        """
        Filter suggestions based on query parameters.
        Supports filtering by minimum confidence and days back.
        """
        queryset = TaskSuggestion.objects.filter(accepted=False)
        
        # Filter by minimum confidence score
        min_confidence = self.request.query_params.get('min_confidence')
        if min_confidence:
            queryset = queryset.filter(confidence_score__gte=float(min_confidence))
        
        # Filter by days back
        days_back = self.request.query_params.get('days_back')
        if days_back:
            cutoff_date = datetime.now() - timedelta(days=int(days_back))
            queryset = queryset.filter(created_at__gte=cutoff_date)
        
        return queryset

@api_view(['POST'])
def accept_task_suggestion(request, suggestion_id):
    """
    Accept a task suggestion and create a new task from it.
    
    POST: Accepts a suggestion and creates a corresponding task
    """
    try:
        suggestion = TaskSuggestion.objects.get(id=suggestion_id)
        
        # Create a new task from the suggestion
        task = Task.objects.create(
            title=suggestion.title,
            description=suggestion.description,
            priority=suggestion.suggested_priority,
            deadline=suggestion.suggested_deadline
        )
        
        # Mark suggestion as accepted
        suggestion.accepted = True
        suggestion.save()
        
        return Response(
            {'message': 'Task created successfully', 'task_id': task.id},
            status=status.HTTP_201_CREATED
        )
        
    except TaskSuggestion.DoesNotExist:
        return Response(
            {'error': 'Suggestion not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )