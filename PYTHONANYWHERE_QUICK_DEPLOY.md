# PythonAnywhere Deployment - Quick Checklist

## ⚡ Quick Deploy in 15 Minutes

### Step 1: Push to GitHub (5 min)

```bash
cd c:\Users\ADMIN\Downloads\movie_recommendation_api-1

git init
git add .
git commit -m "Movie Recommendation API"
git remote add origin https://github.com/YOUR_USERNAME/movie_recommendation_api.git
git branch -M main
git push -u origin main
```

**Get GitHub Token:**
1. https://github.com/settings/tokens
2. Generate new token (select `repo`)
3. Use as password when prompted

---

### Step 2: Create PythonAnywhere Account (2 min)

1. Go to https://www.pythonanywhere.com
2. Sign up (free account)
3. Verify email
4. Log in

---

### Step 3: Clone on PythonAnywhere (2 min)

1. Click **"Consoles"** → **"Bash"**
2. Run:
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/movie_recommendation_api.git
cd movie_recommendation_api
```

---

### Step 4: Setup Virtual Environment (3 min)

```bash
mkvirtualenv --python=/usr/bin/python3.10 mymovieapi
workon mymovieapi
pip install -r requirements.txt
```

Wait for installation to complete.

---

### Step 5: Create Production Settings File

Create file: `config/settings/pythonanywhere.py`

```python
from .base import *
import os

DEBUG = False
ALLOWED_HOSTS = ['YOUR_USERNAME.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = [
    'https://YOUR_USERNAME.pythonanywhere.com',
]

SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
```

---

### Step 6: Run Migrations (2 min)

In Bash console:

```bash
cd ~/movie_recommendation_api
workon mymovieapi
python manage.py migrate --settings=config.settings.pythonanywhere
python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere
python manage.py createsuperuser --settings=config.settings.pythonanywhere
```

---

### Step 7: Configure Web App (1 min)

1. Click **"Web"** tab
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"**
4. Select **"Python 3.10"**

---

### Step 8: Edit WSGI File (1 min)

1. In Web tab, click WSGI file path
2. Replace content with:

```python
import os
import sys

path = '/home/YOUR_USERNAME/movie_recommendation_api'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings.pythonanywhere'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

Replace `YOUR_USERNAME` with your PythonAnywhere username.

---

### Step 9: Configure Virtual Environment (1 min)

In Web tab:
1. Find **"Virtualenv"**
2. Enter: `/home/YOUR_USERNAME/.virtualenvs/mymovieapi`
3. Click checkmark

---

### Step 10: Configure Static Files (1 min)

In Web tab:
1. Click **"Add a new static files mapping"**
2. URL: `/static/`
3. Directory: `/home/YOUR_USERNAME/movie_recommendation_api/static`
4. Click checkmark

---

### Step 11: Reload & Test (1 min)

1. Click green **"Reload"** button
2. Wait 10 seconds
3. Visit: `https://YOUR_USERNAME.pythonanywhere.com/api/docs/`

---

## ✅ Done! Your API is Live!

### Your Live URLs:

- **Swagger Docs**: `https://YOUR_USERNAME.pythonanywhere.com/api/docs/`
- **ReDoc**: `https://YOUR_USERNAME.pythonanywhere.com/api/redoc/`
- **Admin**: `https://YOUR_USERNAME.pythonanywhere.com/admin/`
- **API**: `https://YOUR_USERNAME.pythonanywhere.com/api/`

---

## 🔑 Add TMDb API Key

In Bash console:

```bash
cd ~/movie_recommendation_api
nano .env
```

Add:
```
TMDB_API_KEY=your-api-key-here
```

Save: `Ctrl+X` → `Y` → `Enter`

Then reload web app.

---

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError | Run: `workon mymovieapi` |
| Static files not loading | Run: `python manage.py collectstatic --noinput --settings=config.settings.pythonanywhere` |
| 502 Bad Gateway | Check error logs in Web tab, then reload |
| Allowed host error | Update `ALLOWED_HOSTS` in pythonanywhere.py |

---

## 📝 Important Notes

- Replace `YOUR_USERNAME` with your actual PythonAnywhere username
- Free tier: 100 requests/day, 512MB disk
- Upgrade to paid for unlimited
- Use HTTPS (automatically provided)

---

## 🎉 Share Your Live API!

Once deployed, share this link:
```
https://YOUR_USERNAME.pythonanywhere.com/api/docs/
```

Anyone can now test your Movie Recommendation API!

---

**Need help?** See `docs/PYTHONANYWHERE_DEPLOYMENT.md` for detailed guide.
