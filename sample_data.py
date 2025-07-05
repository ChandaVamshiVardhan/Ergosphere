#!/usr/bin/env python
"""
Sample data script for Smart Todo application.
Run this script to populate the database with sample tasks and categories.
"""

import os
import sys
import django
from datetime import datetime, timedelta

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_todo.settings')
django.setup()

from tasks.models import Task, Category, DailyContext
from ai_module.task_ai import task_ai

def create_sample_categories():
    """Create sample categories"""
    categories = [
        {'name': 'Work', 'color': '#3B82F6'},
        {'name': 'Personal', 'color': '#10B981'},
        {'name': 'Health', 'color': '#EF4444'},
        {'name': 'Finance', 'color': '#F59E0B'},
        {'name': 'Education', 'color': '#8B5CF6'},
        {'name': 'Shopping', 'color': '#EC4899'},
        {'name': 'Travel', 'color': '#06B6D4'},
        {'name': 'Home', 'color': '#84CC16'},
    ]
    
    created_categories = []
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'color': cat_data['color']}
        )
        created_categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    return created_categories

def create_sample_tasks(categories):
    """Create sample tasks"""
    work_cat = next((cat for cat in categories if cat.name == 'Work'), None)
    personal_cat = next((cat for cat in categories if cat.name == 'Personal'), None)
    health_cat = next((cat for cat in categories if cat.name == 'Health'), None)
    finance_cat = next((cat for cat in categories if cat.name == 'Finance'), None)
    
    tasks_data = [
        {
            'title': 'Complete Project Proposal',
            'description': 'Finish the quarterly project proposal for the new client. Include budget estimates and timeline.',
            'category': work_cat,
            'priority': 'high',
            'status': 'pending',
            'deadline': datetime.now() + timedelta(days=3),
            'estimated_duration': 120,
            'tags': ['work', 'proposal', 'client'],
            'ai_priority_score': 0.85,
        },
        {
            'title': 'Schedule Doctor Appointment',
            'description': 'Book annual checkup with Dr. Smith. Need to get blood work done as well.',
            'category': health_cat,
            'priority': 'medium',
            'status': 'pending',
            'deadline': datetime.now() + timedelta(days=7),
            'estimated_duration': 30,
            'tags': ['health', 'appointment', 'checkup'],
            'ai_priority_score': 0.65,
        },
        {
            'title': 'Pay Electricity Bill',
            'description': 'Electricity bill is due this week. Amount: $85.50',
            'category': finance_cat,
            'priority': 'urgent',
            'status': 'pending',
            'deadline': datetime.now() + timedelta(days=1),
            'estimated_duration': 15,
            'tags': ['finance', 'bill', 'urgent'],
            'ai_priority_score': 0.95,
        },
        {
            'title': 'Buy Groceries',
            'description': 'Need to buy groceries for the week. Items: milk, bread, vegetables, fruits.',
            'category': personal_cat,
            'priority': 'medium',
            'status': 'pending',
            'deadline': datetime.now() + timedelta(days=2),
            'estimated_duration': 60,
            'tags': ['personal', 'shopping', 'groceries'],
            'ai_priority_score': 0.55,
        },
        {
            'title': 'Review Code Changes',
            'description': 'Review pull request #123 for the new authentication feature. Check for security issues.',
            'category': work_cat,
            'priority': 'high',
            'status': 'in_progress',
            'deadline': datetime.now() + timedelta(days=1),
            'estimated_duration': 90,
            'tags': ['work', 'code-review', 'security'],
            'ai_priority_score': 0.80,
        },
        {
            'title': 'Plan Weekend Trip',
            'description': 'Plan details for the weekend trip to the mountains. Book accommodation and activities.',
            'category': personal_cat,
            'priority': 'low',
            'status': 'pending',
            'deadline': datetime.now() + timedelta(days=10),
            'estimated_duration': 45,
            'tags': ['personal', 'travel', 'planning'],
            'ai_priority_score': 0.40,
        },
        {
            'title': 'Update Resume',
            'description': 'Update resume with recent project experience and new skills learned.',
            'category': work_cat,
            'priority': 'medium',
            'status': 'pending',
            'deadline': datetime.now() + timedelta(days=5),
            'estimated_duration': 60,
            'tags': ['work', 'resume', 'career'],
            'ai_priority_score': 0.70,
        },
        {
            'title': 'Call Mom',
            'description': 'Call mom to check in and discuss family plans for next month.',
            'category': personal_cat,
            'priority': 'medium',
            'status': 'completed',
            'deadline': datetime.now() - timedelta(days=1),
            'estimated_duration': 20,
            'tags': ['personal', 'family', 'call'],
            'ai_priority_score': 0.60,
        },
    ]
    
    created_tasks = []
    for task_data in tasks_data:
        task = Task.objects.create(**task_data)
        created_tasks.append(task)
        print(f"Created task: {task.title}")
    
    return created_tasks

def create_sample_context():
    """Create sample daily context entries"""
    context_data = [
        {
            'content': 'Meeting with client tomorrow at 2 PM. Need to prepare presentation slides and budget estimates.',
            'context_type': 'meeting',
            'sender': 'John Manager',
            'subject': 'Client Meeting Tomorrow',
            'keywords': ['meeting', 'client', 'presentation', 'budget'],
            'sentiment_score': 0.3,
            'urgency_score': 0.8,
            'processed': True,
        },
        {
            'content': 'Received email from HR about annual performance review. Deadline is next Friday.',
            'context_type': 'email',
            'sender': 'HR Department',
            'subject': 'Annual Performance Review',
            'keywords': ['performance', 'review', 'deadline', 'hr'],
            'sentiment_score': 0.1,
            'urgency_score': 0.7,
            'processed': True,
        },
        {
            'content': 'WhatsApp message from friend: "Hey, are you free this weekend? Thinking of going hiking."',
            'context_type': 'whatsapp',
            'sender': 'Sarah Friend',
            'subject': 'Weekend Plans',
            'keywords': ['weekend', 'hiking', 'friend', 'plans'],
            'sentiment_score': 0.6,
            'urgency_score': 0.2,
            'processed': True,
        },
        {
            'content': 'Note to self: Need to buy birthday gift for sister. Her birthday is in 2 weeks.',
            'context_type': 'note',
            'sender': 'Self',
            'subject': 'Birthday Gift Reminder',
            'keywords': ['birthday', 'gift', 'sister', 'reminder'],
            'sentiment_score': 0.4,
            'urgency_score': 0.4,
            'processed': True,
        },
        {
            'content': 'Phone call from dentist office: Appointment reminder for next Tuesday at 3 PM.',
            'context_type': 'call',
            'sender': 'Dental Office',
            'subject': 'Appointment Reminder',
            'keywords': ['dentist', 'appointment', 'reminder', 'tuesday'],
            'sentiment_score': 0.0,
            'urgency_score': 0.5,
            'processed': True,
        },
    ]
    
    created_context = []
    for context_item in context_data:
        context = DailyContext.objects.create(**context_item)
        created_context.append(context)
        print(f"Created context: {context.context_type} - {context.subject}")
    
    return created_context

def main():
    """Main function to create sample data"""
    print("Creating sample data for Smart Todo application...")
    print("=" * 50)
    
    # Create categories
    print("\n1. Creating categories...")
    categories = create_sample_categories()
    
    # Create tasks
    print("\n2. Creating tasks...")
    tasks = create_sample_tasks(categories)
    
    # Create context entries
    print("\n3. Creating daily context entries...")
    context_entries = create_sample_context()
    
    print("\n" + "=" * 50)
    print("Sample data creation completed!")
    print(f"Created {len(categories)} categories")
    print(f"Created {len(tasks)} tasks")
    print(f"Created {len(context_entries)} context entries")
    print("\nYou can now run the application and see the sample data.")
    print("Backend: http://localhost:8000")
    print("Frontend: http://localhost:3000")

if __name__ == '__main__':
    main() 