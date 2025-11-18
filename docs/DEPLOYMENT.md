# Deployment Guide

## Pre-Deployment Checklist

- [ ] All tests pass: `python manage.py test`
- [ ] Security checks pass: `python manage.py check --deploy`
- [ ] Environment variables are configured
- [ ] Database migrations are up to date
- [ ] Static files are collected
- [ ] Media files are configured
- [ ] HTTPS/SSL is configured
- [ ] Email settings are configured
- [ ] Logging is configured
- [ ] Backup strategy is in place

## Environment Variables for Production

Create a `.env` file with production values:

```env
# Django
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
POSTGRES_DB=movie_db_prod
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=very-secure-password
POSTGRES_HOST=your-db-host.com
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://your-redis-host.com:6379/0

# TMDb API
TMDB_API_KEY=your-tmdb-api-key

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

## Deployment Options

### 1. Heroku Deployment

#### Prerequisites
- Heroku CLI installed
- Heroku account

#### Steps

1. **Create Heroku app:**
```bash
heroku create your-app-name
```

2. **Add PostgreSQL addon:**
```bash
heroku addons:create heroku-postgresql:standard-0
```

3. **Add Redis addon:**
```bash
heroku addons:create heroku-redis:premium-0
```

4. **Set environment variables:**
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
heroku config:set TMDB_API_KEY=your-tmdb-key
# ... set other variables
```

5. **Create Procfile:**
```
web: gunicorn config.wsgi --log-file -
release: python manage.py migrate
```

6. **Deploy:**
```bash
git push heroku main
```

### 2. AWS EC2 Deployment

#### Prerequisites
- AWS account
- EC2 instance running Ubuntu 20.04 or later

#### Steps

1. **SSH into your instance:**
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

2. **Update system:**
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

3. **Install dependencies:**
```bash
sudo apt-get install -y python3.11 python3.11-venv python3-pip
sudo apt-get install -y postgresql postgresql-contrib
sudo apt-get install -y redis-server
sudo apt-get install -y nginx
sudo apt-get install -y supervisor
```

4. **Clone repository:**
```bash
git clone https://github.com/your-username/movie_recommendation_api.git
cd movie_recommendation_api
```

5. **Create virtual environment:**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

6. **Install Python dependencies:**
```bash
pip install -r requirements.txt
pip install gunicorn
```

7. **Configure environment:**
```bash
cp .env.example .env
nano .env  # Edit with production values
```

8. **Run migrations:**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

9. **Create Gunicorn systemd service:**
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon for movie_recommendation_api
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/movie_recommendation_api
ExecStart=/home/ubuntu/movie_recommendation_api/venv/bin/gunicorn \
          --workers 4 \
          --bind unix:/home/ubuntu/movie_recommendation_api/gunicorn.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

10. **Enable and start Gunicorn:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

11. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/movie_api
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/ubuntu/movie_recommendation_api/staticfiles/;
    }

    location /media/ {
        alias /home/ubuntu/movie_recommendation_api/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/movie_recommendation_api/gunicorn.sock;
    }
}
```

12. **Enable Nginx site:**
```bash
sudo ln -s /etc/nginx/sites-available/movie_api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

13. **Set up SSL with Let's Encrypt:**
```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 3. Docker Deployment

#### Build Docker image:
```bash
docker build -t movie-api:latest .
```

#### Run container:
```bash
docker run -d \
  --name movie_api \
  -p 8000:8000 \
  --env-file .env \
  movie-api:latest
```

#### Using Docker Compose for production:
```bash
docker-compose -f docker-compose.yml up -d
```

### 4. DigitalOcean App Platform

1. **Connect your GitHub repository**
2. **Configure build settings:**
   - Build command: `pip install -r requirements.txt && python manage.py migrate`
   - Run command: `gunicorn config.wsgi:application --bind 0.0.0.0:8080`

3. **Set environment variables** in the App Platform dashboard

4. **Deploy** by pushing to your repository

## Post-Deployment

### 1. Verify Deployment

```bash
curl https://your-domain.com/api/docs/
```

### 2. Set up Monitoring

- Use CloudWatch (AWS), Datadog, or New Relic
- Monitor CPU, memory, and database performance
- Set up alerts for errors and performance issues

### 3. Set up Logging

- Configure centralized logging (ELK Stack, Splunk, etc.)
- Monitor application logs for errors
- Set up log rotation

### 4. Set up Backups

- Automated PostgreSQL backups (daily)
- Automated Redis snapshots
- Test backup restoration regularly

### 5. Set up CI/CD

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Run tests
      run: |
        python -m pip install -r requirements.txt
        python manage.py test
    
    - name: Deploy to Heroku
      env:
        HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
      run: |
        git push https://heroku:$HEROKU_API_KEY@git.heroku.com/your-app-name.git main
```

## Scaling

### Horizontal Scaling
- Add more Gunicorn workers
- Use load balancer (AWS ELB, Nginx)
- Scale database with read replicas

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Upgrade database instance
- Increase Redis memory

## Performance Optimization

### Database
- Add indexes on frequently queried fields
- Use database connection pooling
- Optimize slow queries

### Caching
- Increase Redis memory
- Adjust cache TTL based on usage patterns
- Use cache warming for popular data

### API
- Enable gzip compression
- Use CDN for static files
- Implement rate limiting

## Troubleshooting

### High Memory Usage
```bash
# Check memory usage
free -h

# Check process memory
ps aux | grep gunicorn
```

### Database Connection Issues
```bash
# Check PostgreSQL connection
psql -h your-db-host -U postgres -d movie_db -c "SELECT 1"
```

### Redis Connection Issues
```bash
# Check Redis connection
redis-cli -h your-redis-host ping
```

### Slow Queries
```bash
# Enable query logging
python manage.py shell
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    # Run your query
    pass

for query in context:
    print(query['sql'], query['time'])
```

## Security Hardening

1. **Update all dependencies regularly:**
```bash
pip list --outdated
pip install --upgrade package-name
```

2. **Run security checks:**
```bash
python manage.py check --deploy
```

3. **Enable HTTPS/SSL** (Let's Encrypt)

4. **Configure CORS properly:**
```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

5. **Set secure headers:**
```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

6. **Use environment variables** for sensitive data

7. **Enable firewall rules** on your server

8. **Regular security audits** and penetration testing
