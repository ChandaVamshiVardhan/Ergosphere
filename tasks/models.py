"""
Django models for the tasks app in Smart Todo.

This module defines the database schema for tasks, categories, daily context,
and task suggestions. All models include timestamps and appropriate relationships.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json

class Category(models.Model):
    """
    Model for task categories.
    
    Categories help organize tasks and can be used for filtering and grouping.
    Each category has a name, color for UI display, and creation timestamp.
    """
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Task(models.Model):
    """
    Main Task model for Smart Todo.
    
    Represents a task with title, description, priority, status, deadline,
    and AI-enhanced features like priority scores and enhanced descriptions.
    """
    # Priority choices for tasks
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Status choices for tasks
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Basic task fields
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    
    # Time-related fields
    deadline = models.DateTimeField(null=True, blank=True)
    estimated_duration = models.IntegerField(help_text="Duration in minutes", null=True, blank=True)
    
    # AI-enhanced fields
    tags = models.JSONField(default=list, blank=True)  # Store tags as JSON array
    ai_priority_score = models.FloatField(default=0.0)  # AI-computed priority score (0-1)
    ai_enhanced_description = models.TextField(blank=True)  # AI-generated description
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-ai_priority_score', '-created_at']  # Order by AI priority, then creation date
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically set completed_at when status changes to completed.
        """
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

class DailyContext(models.Model):
    """
    Model for daily context entries.
    
    Stores various types of daily communications and notes that can be analyzed
    by AI to extract tasks, deadlines, and other relevant information.
    """
    # Context type choices
    CONTEXT_TYPES = [
        ('whatsapp', 'WhatsApp Message'),
        ('email', 'Email'),
        ('note', 'Personal Note'),
        ('meeting', 'Meeting'),
        ('call', 'Phone Call'),
    ]
    
    # Content and metadata
    content = models.TextField()  # The actual content/message
    context_type = models.CharField(max_length=20, choices=CONTEXT_TYPES)
    timestamp = models.DateTimeField(default=timezone.now)
    sender = models.CharField(max_length=100, blank=True)  # Who sent/wrote it
    subject = models.CharField(max_length=200, blank=True)  # Subject/title
    
    # AI analysis results
    keywords = models.JSONField(default=list, blank=True)  # Extracted keywords
    sentiment_score = models.FloatField(default=0.0)  # Sentiment analysis score (-1 to 1)
    urgency_score = models.FloatField(default=0.0)  # Urgency assessment (0 to 1)
    processed = models.BooleanField(default=False)  # Whether AI has processed this
    
    class Meta:
        ordering = ['-timestamp']  # Most recent first
    
    def __str__(self):
        return f"{self.context_type} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

class TaskSuggestion(models.Model):
    """
    Model for AI-generated task suggestions.
    
    Stores suggestions created by AI based on daily context analysis.
    Users can accept these suggestions to create actual tasks.
    """
    # Suggestion details
    title = models.CharField(max_length=200)
    description = models.TextField()
    suggested_category = models.CharField(max_length=100)
    suggested_priority = models.CharField(max_length=10)
    suggested_deadline = models.DateTimeField(null=True, blank=True)
    
    # AI confidence and metadata
    confidence_score = models.FloatField()  # How confident AI is (0-1)
    based_on_context = models.ForeignKey(DailyContext, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)  # Whether user accepted this suggestion
    
    class Meta:
        ordering = ['-confidence_score', '-created_at']  # Highest confidence first
    
    def __str__(self):
        return self.title
