from .settings import *
import dj_database_url
import os
from django.core.exceptions import ImproperlyConfigured

# Ensure we're not using the default development key in production
if SECRET_KEY == 'django-insecure-default-dev-key-123':
    raise ImproperlyConfigured("Production SECRET_KEY must be set in environment")

# Force DEBUG to False in production
DEBUG = False

# Handle ALLOWED_HOSTS more safely
allowed_hosts = os.getenv('ALLOWED_HOSTS', '')
if allowed_hosts:
    ALLOWED_HOSTS = allowed_hosts.split(',')
else:
    ALLOWED_HOSTS = ['.onrender.com']

# Configure database using DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Get frontend URL from environment
FRONTEND_URL = os.getenv('FRONTEND_URL', '')

# Update CORS settings
CORS_ALLOWED_ORIGINS = [
    "https://car-auction-ww5s.onrender.com",  # Your frontend URL
]

# Additional CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# Media files (Render specific)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/' 