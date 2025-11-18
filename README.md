# Movie Recommendation API

A production-grade backend service for a movie recommendation application. Built using Django, PostgreSQL, Redis, and JWT authentication, this service provides performant APIs for trending movies, personalized recommendations, user management, and storing favorite movies. All endpoints are documented with Swagger.

## Project Overview

This backend powers a movie recommendation platform with a focus on:

- **High-performance API design** - Optimized endpoints with pagination and filtering
- **Secure authentication** - JWT-based user authentication and authorization
- **External API integration** - TMDb API integration for movie data
- **Efficient caching** - Redis caching for heavy movie data
- **Comprehensive API documentation** - Swagger UI for easy frontend integration

The project follows real-world backend engineering practices including environment configuration, external API consumption, caching, ORM optimization, and continuous documentation.

## Project Goals

### 1. API Creation
- Endpoints for trending movies
- Endpoints for recommended movies
- TMDb API integration
- Structured error handling and response normalization

### 2. User Management
- JWT-based authentication
- User registration and login
- Users can save and retrieve favorite movies
- User profile management

### 3. Performance Optimization
- Redis caching for:
  - Trending movie responses
  - Recommended movie responses
  - Popular and top-rated movies
- Reduced external API calls
- Lower response latency

### 4. Documentation
- Swagger UI at `/api/docs`
- Auto-generated OpenAPI schema
- ReDoc documentation at `/api/redoc`

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| Django | Core backend framework |
| Django REST Framework | API development |
| PostgreSQL | Relational database |
| Redis | Caching engine |
| TMDb API | External movie data |
| Swagger / drf-yasg | API documentation |
| JWT | Authentication |

## Key Features

### Movie Recommendation API
- Fetch trending movies (daily/weekly)
- Fetch popular movies
- Fetch top-rated movies
- Search movies by title
- Get recommendations based on specific movie
- Robust error handling for rate limits, timeouts, and malformed responses

### User Authentication & Preferences
- JWT authentication with access and refresh tokens
- User registration and login
- Store and retrieve favorite movies
- Rate movies with reviews
- Secure user-isolated data

### Performance Optimization
- Redis caching layer for movie responses
- Configurable cache expiration policies (15 minutes default)
- Reduced load on external APIs
- Database query optimization with indexes

### API Documentation
- Auto-generated Swagger UI
- OpenAPI-compliant documentation
- Available at `/api/docs`
- ReDoc documentation at `/api/redoc`

## Project Structure

```
movie_recommendation_api/
│
├── config/                       # Django project settings
│   ├── settings/
│   │   ├── base.py              # Base settings
│   │   ├── development.py       # Development settings
│   │   └── production.py        # Production settings
│   ├── urls.py                  # Main URL configuration
│   ├── wsgi.py                  # WSGI configuration
│   └── asgi.py                  # ASGI configuration
│
├── apps/
│   ├── movies/                  # Movie API logic
│   │   ├── models.py            # Movie, UserFavoriteMovie, MovieRating models
│   │   ├── views.py             # API views
│   │   ├── serializers.py       # DRF serializers
│   │   ├── urls.py              # Movie app URLs
│   │   ├── tmdb_client.py       # TMDb API client
│   │   ├── admin.py             # Django admin configuration
│   │   └── tests.py             # Unit tests
│   │
│   └── users/                   # Auth & user management
│       ├── models.py            # Custom User model
│       ├── views.py             # User views
│       ├── serializers.py       # User serializers
│       ├── urls.py              # User app URLs
│       ├── admin.py             # Django admin configuration
│       └── tests.py             # Unit tests
│
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (local)
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # This file