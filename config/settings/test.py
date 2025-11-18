"""
Test settings for movie_recommendation_api project.
Uses SQLite for easy testing without PostgreSQL.
"""

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Disable Redis for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable SSL redirect in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
