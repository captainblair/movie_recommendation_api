# Deploy to Render - Quick Guide (5 Minutes)

Render is MUCH better than PythonAnywhere for this project!

## Why Render?

✅ **1 GB disk space** (PythonAnywhere only has 512 MB)
✅ **Unlimited requests** (PythonAnywhere has 100/day limit)
✅ **Free PostgreSQL database**
✅ **Automatic HTTPS**
✅ **GitHub integration** (auto-deploy on push)
✅ **Easy setup**

---

## Step 1: Create Render Account (2 min)

1. Go to https://render.com
2. Click **"Sign up"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render
5. Verify email

---

## Step 2: Push Updated Code to GitHub (1 min)

Your code needs the new Render settings. Run in PowerShell:

```powershell
cd c:\Users\ADMIN\Downloads\movie_recommendation_api-1

git add .
git commit -m "Fix: Use render settings in wsgi.py for Render deployment"
git push origin main
```

**Note:** I've already fixed the `config/wsgi.py` to use `config.settings.render` instead of `config.settings.production`. This ensures Render uses the correct logging configuration (console-only, no file logging).

---

## Step 2.5: Create PostgreSQL Database on Render (IMPORTANT!)

**You MUST create a database first, or the app won't work!**

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Fill in:
   - **Name**: `movie-recommendation-db`
   - **Database**: `movie_db`
   - **User**: `postgres`
   - **Region**: `Oregon (US West)` (same as your Web Service)
   - **Version**: Latest available
4. Click **"Create Database"**
5. **Wait 2-3 minutes** for the database to be created
6. Copy the **Internal Database URL** (you'll need this)

---

## Step 3: Create Web Service on Render (2 min)

1. Log in to Render dashboard
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Search for: `movie_recommendation_api`
5. Click **"Connect"**

---

## Step 4: Configure Service

Fill in these fields:

| Field | Value |
|-------|-------|
| Name | `movie-recommendation-api` |
| Service Type | `Web Service` |
| Language | `Docker` |
| Region | `Oregon (US West)` |
| Branch | `main` |
| Instance Type | `Free` (or `Starter` for production) |
| Root Directory | (Leave empty - use repository root) |

---

## Step 5: Add Environment Variables

⚠️ **IMPORTANT:** Do NOT click **"Add from .env"** - this will import variables with invalid characters that Render rejects.

Instead, click **"Add Environment Variable"** and fill in each variable separately:

| Name | Value |
|------|-------|
| `DEBUG` | `False` |
| `SECRET_KEY` | Generate a random key (see below) |
| `ALLOWED_HOSTS` | `*.onrender.com,localhost,127.0.0.1` |
| `TMDB_API_KEY` | `your-actual-tmdb-api-key` |
| `DATABASE_URL` | Copy from your PostgreSQL database (see below) |

**How to get DATABASE_URL:**
1. Go to your PostgreSQL database in Render
2. Copy the **Internal Database URL** (looks like: `postgresql://user:password@host:5432/dbname`)
3. Paste it as the value for `DATABASE_URL`

**How to generate SECRET_KEY:**

Run this in PowerShell:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or use: https://djecrety.ir/ (click refresh to generate, then copy the key)

The key should be a long random string like: `django-insecure-abc123xyz789...`

**How to fill in each variable:**
1. Enter the **Name** in the left box (e.g., `DEBUG`)
2. Enter the **Value** in the right box (e.g., `False`)
3. Click **"Add Environment Variable"** to add the next one

**Important - Variable Name Rules:**
- Must contain only: letters (A-Z, a-z), digits (0-9), underscore `_`, hyphen `-`, or dot `.`
- Must NOT start with a digit
- Examples of valid names: `DEBUG`, `SECRET_KEY`, `TMDB_API_KEY`, `API.KEY`, `my-var`
- Examples of invalid names: `1DEBUG`, `DEBUG!`, `SECRET KEY` (spaces not allowed)

**Getting your TMDB_API_KEY:**
1. Go to https://www.themoviedb.org/
2. Create an account or log in
3. Click your profile → **Settings** → **API**
4. Click **"Create"** or **"Request an API Key"**
5. Choose **"Developer"** and accept terms
6. Fill in the TMDb Developer Plan form:

| Field | Value |
|-------|-------|
| Application Name | `Movie Recommendation API` |
| Application URL | `https://movie-recommendation-api.onrender.com` |
| Type of Use | Select: **Website** |
| Application Summary | `A Django REST API that provides movie recommendations using TMDb data. Built for educational purposes.` |
| First Name | Your first name |
| Last Name | Your last name |
| Email Address | Your email |
| Phone Number | Your phone number |
| Address 1 | Your street address |
| Address 2 | (Leave empty if not applicable) |
| City | Your city |
| State | Your state/province |
| Zip Code | Your postal code |

7. Click **"Submit"**
8. Copy your API key and paste it as the value for `TMDB_API_KEY`

---

## Step 5a: Advanced Configuration

Click **"Advanced"** and configure:

| Field | Value |
|-------|-------|
| Secret Files | (Leave empty - not needed) |
| Health Check Path | `/api/health/` (or leave empty for default) |
| Registry Credential | `No credential` (using public Docker image) |
| Docker Build Context Directory | (Leave empty - defaults to root) |
| Dockerfile Path | `./Dockerfile` (default) |
| Docker Command | (Leave empty - use Dockerfile CMD) |
| Pre-Deploy Command | `python manage.py migrate` |
| Auto-Deploy | `On Commit` (enabled) |
| Build Filters - Included Paths | (Leave empty - deploy on all changes) |
| Build Filters - Ignored Paths | (Leave empty - no ignored paths) |

---

## Step 6: Deploy!

Click **"Create Web Service"**

Render will:
- Clone your repo
- Install dependencies
- Create database
- Run migrations
- Deploy your app

Wait 5-10 minutes...

---

## Step 7: Access Your API

Render will give you a URL like:

```
https://movie-recommendation-api.onrender.com
```

Visit:
```
https://movie-recommendation-api.onrender.com/api/docs/
```

You should see Swagger UI! 🎉

---

## Your Live URLs

- **Swagger**: `https://movie-recommendation-api.onrender.com/api/docs/`
- **ReDoc**: `https://movie-recommendation-api.onrender.com/api/redoc/`
- **Admin**: `https://movie-recommendation-api.onrender.com/admin/`
- **API**: `https://movie-recommendation-api.onrender.com/api/`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build failed | Check logs in Render dashboard |
| Database error | Render provides free PostgreSQL, check DATABASE_URL |
| Static files not loading | Already configured in render.py |
| 502 error | Wait a bit, app might still be starting |

---

## Done! 🎉

Your API is now live on Render with:
- ✅ 1 GB disk space
- ✅ Free PostgreSQL
- ✅ Unlimited requests
- ✅ HTTPS
- ✅ Auto-deploy on GitHub push

---

## Next Steps

1. Test your API at `/api/docs/`
2. Add TMDb API key to environment variables
3. Share your live URL!

**Much better than PythonAnywhere!** 🚀
