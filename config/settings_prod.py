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

# Remove the dj_database_url configuration and use SQLite instead
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
    },
} 