# Deploy to PythonAnywhere - Complete Guide

PythonAnywhere is an excellent choice for hosting Django applications. It's beginner-friendly and free tier available.

## Prerequisites

- GitHub account (to push your code)
- PythonAnywhere account (free at https://www.pythonanywhere.com)
- Your project on GitHub

## Step 1: Push Your Project to GitHub

### 1.1 Create a GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `movie_recommendation_api`
3. Choose "Public" (so we can clone it)
4. Click "Create repository"

### 1.2 Push Your Code to GitHub

```bash
cd c:\Users\ADMIN\Downloads\movie_recommendation_api-1

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Movie Recommendation API"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/movie_recommendation_api.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note**: You'll be prompted for GitHub credentials. Use a Personal Access Token:
1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select `repo` scope
4. Copy the token and paste it when prompted for password

---

## Step 2: Set Up PythonAnywhere Account

### 2.1 Create Account

1. Go to https://www.pythonanywhere.com
2. Click "Sign up"
3. Create a free account
4. Verify your email

### 2.2 Access PythonAnywhere Dashboard

1. Log in to PythonAnywhere
2. Go to Dashboard
3. You'll see options for Web, Consoles, Files, etc.

---

## Step 3: Clone Your Repository on PythonAnywhere

### 3.1 Open Bash Console

1. Click **"Consoles"** tab
2. Click **"Bash"** to open a terminal

### 3.2 Clone Your Repository

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/movie_recommendation_api.git
cd movie_recommendation_api
```

---

## Step 4: Create Virtual Environment

### 4.1 Create venv

```bash
mkvirtualenv --python=/usr/bin/python3.10 mymovieapi
```

This creates a virtual environment named `mymovieapi` with Python 3.10.

### 4.2 Activate and Install Dependencies

```bash
workon mymovieapi
pip install -r requirements.txt
```

Wait for all packages to install (may take 2-3 minutes).

---

## Step 5: Configure Django Settings

### 5.1 Create Production Settings

Edit `config/settings/pythonanywhere.py`:

```python
from .base import *
import os

DEBUG = False

# Replace with your PythonAnywhere domain
ALLOWED_HOSTS = ['YOUR_USERNAME.pythonanywhere.com']

# Database - Use SQLite for free tier
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Cache - Use local memory
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
X_FRAME_OPTIONS = 'DENY'

# CORS
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    'https://YOUR_USERNAME.pythonanywhere.com',
]

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Secret key from environment
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-your-secret-key-here')
```

### 5.2 Create .env File on PythonAnywhere

In the Bash console:

```bash
cd ~/movie_recommendation_api
cat > .env << 'EOF'
SECRET_KEY=django-insecure-your-very-secret-key-change-this
DEBUG=False
ALLOWED_HOSTS=YOUR_USERNAME.pythonanywhere.com
TMDB_API_KEY=your-tmdb-api-key-here
EOF
```

---

## Step 6: Run Migrations

In the Bash console:

```bash
cd ~/movie_recommendation_api
workon mymovieapi
python manage.py migrate --settings=config.settings.pythonanywhere
python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere
python manage.py createsuperuser --settings=config.settings.pythonanywhere
```

---

## Step 7: Create WSGI File

### 7.1 Go to Web Tab

1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**

### 7.2 Edit WSGI File

1. In the Web tab, find **"WSGI configuration file"**
2. Click the path (e.g., `/var/www/YOUR_USERNAME_pythonanywhere_com_wsgi.py`)
3. Replace the entire content with:

```python
import os
import sys

# Add your project to the path
path = '/home/YOUR_USERNAME/movie_recommendation_api'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.pythonanywhere'

# Import Django WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

### 7.3 Configure Virtual Environment

1. In the Web tab, find **"Virtualenv"**
2. Click the path and enter: `/home/YOUR_USERNAME/.virtualenvs/mymovieapi`
3. Click the checkmark

### 7.4 Configure Static Files

In the Web tab, find **"Static files"** section:

1. Click **"Add a new static files mapping"**
2. URL: `/static/`
3. Directory: `/home/YOUR_USERNAME/movie_recommendation_api/static`
4. Click the checkmark

---

## Step 8: Reload Web App

1. In the Web tab, click the **green "Reload"** button
2. Wait 10-15 seconds for the app to start

---

## Step 9: Test Your Deployment

### 9.1 Visit Your API

Open your browser and go to:
```
https://YOUR_USERNAME.pythonanywhere.com/api/docs/
```

You should see the Swagger UI!

### 9.2 Test Endpoints

1. Click **"Authorize"** button
2. Login with your superuser credentials
3. Try the endpoints!

---

## Step 10: Add TMDb API Key

### 10.1 Get API Key

1. Go to https://www.themoviedb.org/settings/api
2. Create an API key
3. Copy it

### 10.2 Add to PythonAnywhere

1. In Bash console:
```bash
cd ~/movie_recommendation_api
nano .env
```

2. Edit the line:
```
TMDB_API_KEY=your-actual-api-key-here
```

3. Press `Ctrl+X`, then `Y`, then `Enter` to save

4. Reload your web app in the Web tab

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Solution**: Make sure virtual environment is activated:
```bash
workon mymovieapi
```

### Issue: "Static files not loading"

**Solution**: Run collectstatic:
```bash
python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere
```

Then reload the web app.

### Issue: "502 Bad Gateway"

**Solution**: 
1. Check error logs in PythonAnywhere Web tab
2. Make sure WSGI file is correct
3. Reload the web app

### Issue: "Allowed host mismatch"

**Solution**: Update `ALLOWED_HOSTS` in `config/settings/pythonanywhere.py` with your domain.

### Issue: Database errors

**Solution**: Run migrations again:
```bash
python manage.py migrate --settings=config.settings.pythonanywhere
```

---

## Useful PythonAnywhere Commands

### View Error Logs
```bash
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.error.log
```

### View Access Logs
```bash
tail -f /var/log/YOUR_USERNAME.pythonanywhere.com.access.log
```

### Restart Web App
Click the green "Reload" button in the Web tab.

### SSH into Console
Click "Bash" in the Consoles tab.

---

## Your Live API

Once deployed, your API will be at:

```
https://YOUR_USERNAME.pythonanywhere.com/
```

### Live Endpoints:

- **Swagger Docs**: `https://YOUR_USERNAME.pythonanywhere.com/api/docs/`
- **ReDoc**: `https://YOUR_USERNAME.pythonanywhere.com/api/redoc/`
- **Admin**: `https://YOUR_USERNAME.pythonanywhere.com/admin/`
- **API Base**: `https://YOUR_USERNAME.pythonanywhere.com/api/`

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Create PythonAnywhere account
3. ✅ Clone repository on PythonAnywhere
4. ✅ Set up virtual environment
5. ✅ Configure Django settings
6. ✅ Create WSGI file
7. ✅ Test your deployment
8. ✅ Share your live URL!

---

## Share Your Live API

Once live, share this URL:
```
https://YOUR_USERNAME.pythonanywhere.com/api/docs/
```

Anyone can now:
- View your API documentation
- Test your endpoints
- See your live movie recommendation API!

---

## Free Tier Limitations

- 512 MB disk space
- SQLite database (no PostgreSQL)
- No Redis (use local memory cache)
- 100 requests per day (free tier)
- Upgrade to paid for unlimited

---

## Upgrade to Paid (Optional)

If you need more:
- More disk space
- PostgreSQL database
- Redis cache
- Unlimited requests
- Custom domain

Visit: https://www.pythonanywhere.com/pricing/

---

**Your Movie Recommendation API is now live! 🎉**
