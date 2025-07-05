"""
WSGI config for smart_todo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/

This file is used by web servers like Gunicorn or uWSGI to serve the Django application.
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the Django settings module for the WSGI application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_todo.settings')

# Create the WSGI application object
application = get_wsgi_application()


