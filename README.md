# movie_recommendation_api

A production-grade backend service for a movie recommendation application.
Built using Django, PostgreSQL, Redis, and JWT authentication, this service provides performant APIs for trending movies, personalized recommendations, user management, and storing favorite movies. All endpoints are documented with Swagger.

## Project Overview

This backend powers a movie recommendation platform with a focus on:

- High-performance API design
- Secure authentication
- External API integration (TMDb)
- Efficient caching for heavy movie data
- Comprehensive API documentation for frontend integration

The project follows real-world backend engineering practices including environment configuration, external API consumption, caching, ORM optimization, and continuous documentation.

## Project Goals

### 1. API Creation
- Endpoints for trending movies
- Endpoints for recommended movies
- TMDb API integration
- Structured error handling and response normalization

### 2. User Management
- JWT-based authentication
- Users can save and retrieve favorite movies

### 3. Performance Optimization
Redis caching for:
- trending movie responses
- recommended movie responses
- Reduced external API calls
- Lower response latency

### 4. Documentation
- Swagger UI at /api/docs
- Auto-generated OpenAPI schema

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Django | Core backend framework |
| Django REST Framework | API development |
| PostgreSQL | Relational database |
| Redis | Caching engine |
| TMDb API | External movie data |
| Swagger / drf-yasg | API documentation |
| JWT | Authentication |

## Key Features

### Movie Recommendation API
- Fetch trending movies
- Fetch recommended movies
- Use external TMDb API
- Robust error handling for rate limits, timeouts, and malformed responses

### User Authentication & Preferences
- JWT authentication
- User registration and login
- Store and retrieve favorite movies
- Secure user-isolated data

### Performance Optimization
- Redis caching layer for movie responses
- Configurable cache expiration policies
- Reduced load on external APIs

### API Documentation
- Auto-generated Swagger UI
- OpenAPI-compliant documentation
- Available at /api/docs

## Implementation Roadmap

### Initial Setup
- feat: initialize Django project with PostgreSQL configuration
- feat: integrate TMDb API client

### Feature Development
- feat: create movie recommendation endpoints
- feat: implement JWT authentication
- feat: add favorite movie storage

### Performance Optimization
- perf: add Redis caching layer

### Documentation
- feat: integrate Swagger for API documentation
- docs: update README with API reference and setup details

## Project Structure (Planned)

```
movie_recommendation_api/
│
├── config/                       # Django project settings
├── movies/                       # Movie API logic
├── users/                        # Auth & favorites
├── docs/                         # API documentation files
├── requirements.txt
├── README.md
└── docker-compose.yml
```

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/<your-username>/movie_recommendation_api.git
cd movie_recommendation_api
```

### 2. Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a .env file:

```
SECRET_KEY=
DEBUG=True
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
REDIS_URL=redis://localhost:6379
TMDB_API_KEY=
```

### 5. Migrations
```bash
python manage.py migrate
```

### 6. Run Server
```bash
python manage.py runserver
```

Swagger UI → http://127.0.0.1:8000/api/docs/