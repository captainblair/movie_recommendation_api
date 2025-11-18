"""
Development settings for movie_recommendation_api project.
"""

import os
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']

# Database
DATABASES['default']['NAME'] = os.getenv('POSTGRES_DB', 'movie_db_dev')

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Disable SSL redirect in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
