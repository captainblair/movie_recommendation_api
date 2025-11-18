"""
Gunicorn configuration for production deployment.
"""

import multiprocessing
import os

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8000')
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'movie_recommendation_api'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL
keyfile = None
certfile = None
ssl_version = None
cert_reqs = 0
ca_certs = None
suppress_ragged_eof = True

# Application
raw_env = []
