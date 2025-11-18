# Troubleshooting Guide

## Common Issues and Solutions

### 1. Database Connection Issues

#### Problem: `psycopg2.OperationalError: could not connect to server`

**Solution:**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL if not running
sudo systemctl start postgresql

# Verify connection
psql -U postgres -h localhost -d movie_db

# Check .env file for correct database credentials
cat .env | grep POSTGRES
```

#### Problem: `django.db.utils.ProgrammingError: relation "app_model" does not exist`

**Solution:**
```bash
# Run migrations
python manage.py migrate

# Create missing migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 2. Redis Connection Issues

#### Problem: `ConnectionError: Error 111 connecting to localhost:6379`

**Solution:**
```bash
# Check if Redis is running
redis-cli ping

# Start Redis if not running
sudo systemctl start redis-server

# Verify Redis connection
redis-cli -h localhost -p 6379

# Check REDIS_URL in .env
cat .env | grep REDIS_URL
```

#### Problem: Cache not working

**Solution:**
```bash
# Clear Redis cache
redis-cli FLUSHALL

# Check Redis memory usage
redis-cli INFO memory

# Increase Redis memory if needed
# Edit /etc/redis/redis.conf and increase maxmemory
```

### 3. Authentication Issues

#### Problem: `Invalid token` or `Token is invalid or expired`

**Solution:**
```bash
# Generate new token
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# Token expires after 1 hour, use refresh token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "your_refresh_token"}'
```

#### Problem: `Authentication credentials were not provided`

**Solution:**
```bash
# Include Authorization header in requests
curl -H "Authorization: Bearer your_access_token" \
  http://localhost:8000/api/movies/

# Verify token is valid
python manage.py shell
from rest_framework_simplejwt.tokens import AccessToken
token = AccessToken('your_token')
print(token.payload)
```

### 4. API Endpoint Issues

#### Problem: `404 Not Found` on API endpoints

**Solution:**
```bash
# Check URL configuration
python manage.py show_urls

# Verify app is in INSTALLED_APPS
grep -n "apps.movies" config/settings/base.py

# Check URL patterns
cat apps/movies/urls.py
cat config/urls.py
```

#### Problem: `405 Method Not Allowed`

**Solution:**
```bash
# Check allowed methods for endpoint
# GET, POST, PUT, PATCH, DELETE

# Example: POST to trending endpoint (should be GET)
# Wrong: POST /api/movies/trending/
# Correct: GET /api/movies/trending/
```

#### Problem: `400 Bad Request`

**Solution:**
```bash
# Check request body format
# Ensure JSON is valid
python -m json.tool < request.json

# Check required fields
# Review API documentation

# Check field types and values
# Ratings must be 1-10
# Emails must be valid format
```

### 5. TMDb API Issues

#### Problem: `Failed to fetch data from TMDb API`

**Solution:**
```bash
# Check TMDB_API_KEY is set
echo $TMDB_API_KEY

# Verify API key is valid
curl "https://api.themoviedb.org/3/trending/movie/week?api_key=YOUR_API_KEY"

# Check API rate limits
# TMDb allows 40 requests per 10 seconds

# Check internet connection
ping api.themoviedb.org
```

#### Problem: `401 Unauthorized` from TMDb API

**Solution:**
```bash
# Verify API key
# Get new key from https://www.themoviedb.org/settings/api

# Check API key in .env
grep TMDB_API_KEY .env

# Test API key directly
curl "https://api.themoviedb.org/3/movie/550?api_key=YOUR_API_KEY"
```

#### Problem: `429 Too Many Requests` from TMDb API

**Solution:**
```bash
# Wait before making more requests
# TMDb rate limit: 40 requests per 10 seconds

# Implement exponential backoff in code
# Increase cache TTL to reduce API calls

# Check current rate limit status
# Monitor API usage in TMDb dashboard
```

### 6. Performance Issues

#### Problem: Slow API responses

**Solution:**
```bash
# Check database query performance
python manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # Run your query
    pass

for query in context:
    print(f"Time: {query['time']}, SQL: {query['sql']}")

# Add database indexes
python manage.py sqlsequencereset apps.movies | python manage.py dbshell

# Check Redis cache hit rate
redis-cli INFO stats
```

#### Problem: High memory usage

**Solution:**
```bash
# Check process memory
ps aux | grep python

# Check Redis memory
redis-cli INFO memory

# Reduce cache TTL
# Edit CACHE_TTL in settings

# Limit query results with pagination
# Use page_size parameter
```

#### Problem: Timeout errors

**Solution:**
```bash
# Increase timeout settings
# Edit TMDB client timeout

# Check server resources
top
free -h

# Optimize database queries
# Add select_related() and prefetch_related()

# Increase worker processes
# Edit gunicorn workers setting
```

### 7. Static Files Issues

#### Problem: Static files not loading (404)

**Solution:**
```bash
# Collect static files
python manage.py collectstatic --noinput

# Check STATIC_URL and STATIC_ROOT
grep -n "STATIC" config/settings/base.py

# Verify static files directory exists
ls -la staticfiles/

# In production, serve with Nginx
# Check Nginx configuration
```

### 8. Email Issues

#### Problem: Emails not sending

**Solution:**
```bash
# Check email configuration
grep -n "EMAIL" config/settings/base.py

# Test email sending
python manage.py shell
from django.core.mail import send_mail
send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])

# Check email backend
# Development: console backend
# Production: SMTP backend

# Verify SMTP credentials
# Check EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
```

### 9. Migration Issues

#### Problem: `No changes detected in app`

**Solution:**
```bash
# Check for model changes
python manage.py makemigrations --dry-run

# Force migration creation
python manage.py makemigrations --empty apps.movies --name migration_name

# Check migration files
ls apps/movies/migrations/
```

#### Problem: `Conflicting migrations detected`

**Solution:**
```bash
# Show migration history
python manage.py showmigrations

# Merge conflicting migrations
python manage.py makemigrations --merge

# Manually resolve conflicts in migration files
```

### 10. Testing Issues

#### Problem: Tests fail with database errors

**Solution:**
```bash
# Use test database
python manage.py test --keepdb

# Check test database settings
grep -n "TEST" config/settings/base.py

# Run specific test
python manage.py test apps.movies.tests.MovieAPITestCase.test_trending_movies
```

#### Problem: Fixtures not loading

**Solution:**
```bash
# Check fixture file format
cat apps/movies/fixtures/movies.json

# Load fixtures manually
python manage.py loaddata apps/movies/fixtures/movies.json

# Create fixtures from existing data
python manage.py dumpdata apps.movies > apps/movies/fixtures/movies.json
```

### 11. Deployment Issues

#### Problem: `ModuleNotFoundError: No module named 'apps'`

**Solution:**
```bash
# Add project directory to Python path
export PYTHONPATH="${PYTHONPATH}:/path/to/project"

# Or use absolute imports
# Instead of: from apps.movies import models
# Use: from movie_recommendation_api.apps.movies import models
```

#### Problem: `DEBUG=True` in production

**Solution:**
```bash
# Set DEBUG=False in .env
DEBUG=False

# Check settings file
grep -n "DEBUG" config/settings/base.py

# Verify environment variable is loaded
python manage.py shell
from django.conf import settings
print(settings.DEBUG)
```

#### Problem: `ALLOWED_HOSTS` error

**Solution:**
```bash
# Add domain to ALLOWED_HOSTS
# Edit .env: ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Or edit settings file
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### 12. Getting Help

#### Check Logs

```bash
# Django logs
tail -f logs/django.log

# Gunicorn logs
journalctl -u gunicorn -n 50

# Nginx logs
tail -f /var/log/nginx/error.log
tail -f /var/log/nginx/access.log

# PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql.log

# Redis logs
redis-cli MONITOR
```

#### Debug Mode

```bash
# Enable debug logging
python manage.py runserver --verbosity 3

# Django shell for interactive debugging
python manage.py shell
from apps.movies.models import Movie
Movie.objects.all()
```

#### Common Commands

```bash
# Check project structure
tree -L 2

# Verify all dependencies installed
pip check

# Show installed packages
pip list

# Check Django version
python -c "import django; print(django.VERSION)"

# Run security checks
python manage.py check --deploy
```

## Getting Additional Help

- **GitHub Issues:** Open an issue with detailed error information
- **Stack Overflow:** Tag questions with `django`, `django-rest-framework`
- **Django Documentation:** https://docs.djangoproject.com/
- **DRF Documentation:** https://www.django-rest-framework.org/
- **TMDb API Docs:** https://developer.themoviedb.org/docs
