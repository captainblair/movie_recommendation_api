# Quick Start Guide

Get the Movie Recommendation API up and running in minutes!

## Prerequisites

- Python 3.11+
- PostgreSQL 12+
- Redis 6+
- Git

## Installation (5 minutes)

### 1. Clone Repository
```bash
git clone https://github.com/your-username/movie_recommendation_api.git
cd movie_recommendation_api
```

### 2. Run Setup Script

**On Linux/Mac:**
```bash
bash setup.sh
```

**On Windows:**
```bash
setup.bat
```

The setup script will:
- Create virtual environment
- Install dependencies
- Configure environment variables
- Run database migrations
- Create superuser
- Run tests

### 3. Start Development Server
```bash
python manage.py runserver
```

## Access the API

- **API Base URL**: http://localhost:8000/api/
- **Swagger Documentation**: http://localhost:8000/api/docs/
- **ReDoc Documentation**: http://localhost:8000/api/redoc/
- **Django Admin**: http://localhost:8000/admin/

## First Steps

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123"
  }'
```

### 2. Get JWT Token
```bash
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepass123"
  }'
```

Response:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Get Trending Movies
```bash
curl -X GET http://localhost:8000/api/movies/trending/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Search for Movies
```bash
curl -X GET "http://localhost:8000/api/movies/search/?q=fight" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Add Movie to Favorites
```bash
curl -X POST http://localhost:8000/api/movies/1/add_to_favorites/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 6. Rate a Movie
```bash
curl -X POST http://localhost:8000/api/movies/1/rate/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 9,
    "review": "Amazing movie!"
  }'
```

## Using Docker

### Quick Start with Docker Compose
```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Redis cache
- Django API server

Access at: http://localhost:8000

### Stop Services
```bash
docker-compose down
```

## Configuration

### Set TMDb API Key

1. Get API key from https://www.themoviedb.org/settings/api
2. Edit `.env` file:
```env
TMDB_API_KEY=your-api-key-here
```
3. Restart server

### Change Database

Edit `.env`:
```env
POSTGRES_DB=your_db_name
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=your_host
POSTGRES_PORT=5432
```

## Common Commands

### Run Tests
```bash
python manage.py test
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Migrations
```bash
python manage.py migrate
```

### Create New Migration
```bash
python manage.py makemigrations
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Access Django Shell
```bash
python manage.py shell
```

### Fetch Trending Movies (Management Command)
```bash
python manage.py fetch_trending_movies --time-window week --pages 3
```

### Fetch Popular Movies (Management Command)
```bash
python manage.py fetch_popular_movies --pages 3
```

## Troubleshooting

### Database Connection Error
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Start PostgreSQL
sudo systemctl start postgresql
```

### Redis Connection Error
```bash
# Check Redis is running
redis-cli ping

# Start Redis
sudo systemctl start redis-server
```

### Port Already in Use
```bash
# Run on different port
python manage.py runserver 8001
```

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Next Steps

1. **Read Full Documentation**: See `README.md`
2. **Explore API**: Visit http://localhost:8000/api/docs/
3. **Deploy**: Follow `docs/DEPLOYMENT.md`
4. **Contribute**: See `docs/CONTRIBUTING.md`

## Support

- 📖 [API Documentation](docs/API_DOCUMENTATION.md)
- 🚀 [Deployment Guide](docs/DEPLOYMENT.md)
- 🐛 [Troubleshooting](docs/TROUBLESHOOTING.md)
- 🔒 [Security](SECURITY.md)

## Tips

- Use Postman or Insomnia for API testing
- Check logs: `tail -f logs/django.log`
- Monitor Redis: `redis-cli MONITOR`
- Use Django admin for data management

Happy coding! 🎉
