# Deploy to Render - Complete Guide

Render is perfect for Django apps with a generous free tier (1 GB disk space, unlimited requests).

## Why Render?

✅ **1 GB disk space** (vs PythonAnywhere's 512 MB)
✅ **Unlimited requests** (vs PythonAnywhere's 100/day)
✅ **Free PostgreSQL database**
✅ **Free Redis cache**
✅ **Automatic HTTPS**
✅ **Easy deployment**
✅ **GitHub integration**

---

## Prerequisites

- GitHub account (already have it ✅)
- Render account (free at https://render.com)
- Your code on GitHub (already done ✅)

---

## Step 1: Create Render Account

1. Go to https://render.com
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your GitHub
5. Verify email

---

## Step 2: Create Web Service

1. Log in to Render dashboard
2. Click **"New +"** button
3. Select **"Web Service"**
4. Click **"Connect a repository"**
5. Search for: `movie_recommendation_api`
6. Click **"Connect"**

---

## Step 3: Configure Web Service

Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `movie-recommendation-api` |
| **Environment** | `Python 3` |
| **Region** | `Oregon (US West)` |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt && python manage.py migrate --settings=config.settings.render && python manage.py collectstatic --noinput --settings=config.settings.render` |
| **Start Command** | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |

---

## Step 4: Add Environment Variables

Click **"Advanced"** and add these environment variables:

```
DEBUG=False
SECRET_KEY=your-very-secret-key-change-this-12345
ALLOWED_HOSTS=your-service-name.onrender.com
TMDB_API_KEY=your-tmdb-api-key-here
DATABASE_URL=postgresql://...  (Render will provide this)
```

---

## Step 5: Create Production Settings

Create file: `config/settings/render.py`

```python
from .base import *
import os
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = [
    'your-service-name.onrender.com',
    'localhost',
    '127.0.0.1'
]

# Database from Render
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# CORS
CORS_ALLOWED_ORIGINS = [
    'https://your-service-name.onrender.com',
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Secret key
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')

# TMDb API
TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
```

---

## Step 6: Update Requirements

Add to `requirements.txt`:

```
dj-database-url==2.1.0
```

---

## Step 7: Deploy

1. Click **"Create Web Service"** button
2. Render will automatically:
   - Clone your repo
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start your app

3. Wait 5-10 minutes for deployment

---

## Step 8: Check Deployment Status

1. Go to your Render dashboard
2. Click on your service
3. Check the **"Logs"** tab
4. Wait for "Build successful" message

---

## Step 9: Access Your API

Your API will be at:

```
https://your-service-name.onrender.com/api/docs/
```

Render will provide your exact URL in the dashboard.

---

## Troubleshooting

### Build Failed

Check logs in Render dashboard. Common issues:
- Missing dependencies in requirements.txt
- Wrong settings module name
- Database connection error

### Static Files Not Loading

Run in Render console:
```bash
python manage.py collectstatic --noinput --settings=config.settings.render
```

### Database Errors

Render provides a free PostgreSQL database. Check:
1. DATABASE_URL environment variable is set
2. Migrations ran successfully
3. Database credentials are correct

---

## Your Live API

Once deployed:

- **Swagger UI**: `https://your-service-name.onrender.com/api/docs/`
- **ReDoc**: `https://your-service-name.onrender.com/api/redoc/`
- **Admin**: `https://your-service-name.onrender.com/admin/`
- **API**: `https://your-service-name.onrender.com/api/`

---

## Free Tier Benefits

✅ 1 GB disk space
✅ Free PostgreSQL database
✅ Unlimited requests
✅ Automatic HTTPS
✅ GitHub integration
✅ Auto-deploys on push

---

## Upgrade to Paid (Optional)

Render paid plans start at $7/month for:
- More resources
- Priority support
- Custom domains
- Better performance

---

**Your API is now live on Render! 🎉**
