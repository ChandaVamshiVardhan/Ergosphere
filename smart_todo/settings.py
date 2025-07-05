"""
Django settings for Smart Todo project.

This file contains all the configuration settings for the Django application,
including database, installed apps, middleware, and AI configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
# List of all Django applications that are enabled in this Django instance
INSTALLED_APPS = [
    'django.contrib.admin',      # Django admin interface
    'django.contrib.auth',       # Authentication system
    'django.contrib.contenttypes', # Content type system
    'django.contrib.sessions',   # Session framework
    'django.contrib.messages',   # Messaging framework
    'django.contrib.staticfiles', # Static file handling
    'rest_framework',            # Django REST framework
    'corsheaders',              # CORS handling for frontend
    'tasks',                    # Our main tasks app
    'drf_yasg',                # API documentation (Swagger/OpenAPI)
]

# Middleware classes - process request/response globally
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Handle CORS headers
    'django.middleware.security.SecurityMiddleware',  # Security middleware
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling
    'django.middleware.common.CommonMiddleware',  # Common middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Message handling
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]

# Root URL configuration
ROOT_URLCONF = 'smart_todo.urls'

# Database configuration
# Using SQLite for development (change to PostgreSQL for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django REST Framework configuration
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Allow all users for development
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Return JSON responses
    ],
}

# CORS configuration - allow all origins for development
CORS_ALLOW_ALL_ORIGINS = True

# AI Configuration
# OpenAI API key for AI-powered features
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Django Templates configuration (required for admin interface)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images) configuration
STATIC_URL = '/static/'