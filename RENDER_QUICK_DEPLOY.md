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
git commit -m "Add Render deployment configuration"
git push origin main
```

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
| Environment | `Python 3` |
| Region | `Oregon (US West)` |
| Branch | `main` |
| Build Command | `pip install -r requirements.txt && python manage.py migrate --settings=config.settings.render && python manage.py collectstatic --noinput --settings=config.settings.render` |
| Start Command | `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT` |

---

## Step 5: Add Environment Variables

Click **"Advanced"** and add:

```
DEBUG=False
SECRET_KEY=your-very-secret-key-12345-change-this
ALLOWED_HOSTS=movie-recommendation-api.onrender.com
TMDB_API_KEY=your-tmdb-api-key-here
```

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
