"""
Pytest configuration file.
"""

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()
