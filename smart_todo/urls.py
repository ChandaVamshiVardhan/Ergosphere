"""
Main URL configuration for Smart Todo Django project.
Defines the root URL patterns including admin, API endpoints, and API documentation.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configure Swagger/OpenAPI schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Smart Todo API",
        default_version='v1',
        description="API documentation for Smart Todo",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Main URL patterns for the application
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints (includes all task-related URLs)
    path('api/', include('tasks.urls')),
    
    # API documentation endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]