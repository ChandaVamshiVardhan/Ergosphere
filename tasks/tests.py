"""
Test suite for the tasks app in Smart Todo.

This module contains unit tests and integration tests for the API endpoints,
AI functionality, and model behavior. Uses Django's TestCase and APITestCase.
"""

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task, Category, DailyContext
from django.utils import timezone

class TaskAPITest(APITestCase):
    """
    Test class for Task API endpoints.
    
    Tests CRUD operations, filtering, and AI suggestion endpoints.
    Uses APITestCase for testing REST API functionality.
    """
    
    def setUp(self):
        """
        Set up test data before each test method.
        Creates a test category and task for use in tests.
        """
        self.category = Category.objects.create(name='Test Category')
        self.task = Task.objects.create(
            title='Test Task',
            description='Test Description',
            category=self.category,
            priority='high'
        )
    
    def test_get_tasks(self):
        """
        Test GET request to retrieve list of tasks.
        Verifies that the API returns the correct number of tasks.
        """
        url = reverse('task-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_task(self):
        """
        Test POST request to create a new task.
        Verifies that tasks can be created successfully and count increases.
        """
        url = reverse('task-list-create')
        data = {
            'title': 'New Task',
            'description': 'New Description',
            'category': self.category.id,
            'priority': 'medium'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)
    
    def test_ai_suggestions(self):
        """
        Test AI suggestions endpoint.
        Verifies that the AI suggestions API responds correctly to prioritization requests.
        """
        url = reverse('ai-suggestions')
        data = {
            'action': 'prioritize',
            'context_data': {
                'content': 'urgent task needed',
                'urgency_score': 0.9
            }
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('prioritized_tasks', response.data)

class AIModuleTest(TestCase):
    """
    Test class for AI module functionality.
    
    Tests the SmartTaskAI class methods for context analysis and task categorization.
    Uses regular TestCase for testing business logic.
    """
    
    def setUp(self):
        """
        Set up AI instance before each test method.
        Initializes the SmartTaskAI class for testing.
        """
        from ai_module.task_ai import SmartTaskAI
        self.ai = SmartTaskAI()
    
    def test_context_analysis(self):
        """
        Test context analysis functionality.
        Verifies that the AI can analyze context and extract urgency and keywords.
        """
        context_data = {
            'content': 'urgent meeting tomorrow with client',
            'context_type': 'whatsapp'
        }
        analysis = self.ai.analyze_context(context_data)
        
        # Verify analysis structure and content
        self.assertIsInstance(analysis, dict)
        self.assertIn('urgency_score', analysis)
        self.assertIn('keywords', analysis)
        self.assertGreater(analysis['urgency_score'], 0)
    
    def test_task_categorization(self):
        """
        Test task categorization functionality.
        Verifies that the AI can categorize tasks based on their content.
        """
        task_data = {
            'title': 'Buy groceries',
            'description': 'Weekly shopping for food items'
        }
        categorization = self.ai.categorize_task(task_data)
        
        # Verify categorization structure and logic
        self.assertIsInstance(categorization, dict)
        self.assertIn('suggested_category', categorization)
        self.assertEqual(categorization['suggested_category'], 'shopping')