# Architecture Documentation

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│              (Web, Mobile, Desktop, etc.)                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Nginx (Reverse Proxy)                     │
│              (Load Balancing, SSL/TLS)                       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                  Gunicorn WSGI Server                        │
│              (Multiple Worker Processes)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Django Application                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  URL Router → Views → Serializers → Models          │   │
│  │  ├─ Authentication (JWT)                            │   │
│  │  ├─ Permissions & Authorization                     │   │
│  │  ├─ Error Handling                                  │   │
│  │  └─ Logging                                         │   │
│  └──────────────────────────────────────────────────────┘   │
└────┬─────────────────────────────────────────────────┬──────┘
     │                                                 │
     │                                                 │
┌────▼──────────────────┐              ┌──────────────▼──────┐
│   PostgreSQL Database  │              │   Redis Cache       │
│  ┌──────────────────┐  │              │  ┌──────────────┐   │
│  │ Users Table      │  │              │  │ Cached Data  │   │
│  │ Movies Table     │  │              │  │ Sessions     │   │
│  │ Favorites Table  │  │              │  │ Tokens       │   │
│  │ Ratings Table    │  │              │  └──────────────┘   │
│  └──────────────────┘  │              └─────────────────────┘
└────────────────────────┘
         │
         │ (External API Calls)
         │
    ┌────▼──────────────┐
    │  TMDb API         │
    │  (Movie Data)     │
    └───────────────────┘
```

## Component Architecture

### 1. API Layer
- **URL Router** (`config/urls.py`)
  - Routes HTTP requests to appropriate views
  - Handles API versioning
  - Manages Swagger documentation

- **Views** (`apps/*/views.py`)
  - ViewSets for CRUD operations
  - Custom actions for special endpoints
  - Request/response handling

- **Serializers** (`apps/*/serializers.py`)
  - Data validation
  - Serialization/deserialization
  - Field-level and object-level validation

### 2. Business Logic Layer
- **Models** (`apps/*/models.py`)
  - Data models
  - Database relationships
  - Business logic methods

- **TMDb Client** (`apps/movies/tmdb_client.py`)
  - External API integration
  - Request handling
  - Error management

### 3. Data Access Layer
- **Django ORM**
  - Query optimization
  - Database abstraction
  - Transaction management

- **Database** (PostgreSQL)
  - Data persistence
  - Relationships
  - Indexing

### 4. Caching Layer
- **Redis**
  - Query result caching
  - Session storage
  - Token blacklisting

### 5. Security Layer
- **Authentication** (JWT)
  - Token generation
  - Token validation
  - Token refresh

- **Authorization** (Permissions)
  - Role-based access control
  - Object-level permissions
  - Custom permission classes

- **Validation**
  - Input validation
  - Data sanitization
  - Error handling

## Data Flow

### User Registration Flow
```
1. Client sends registration request
   ↓
2. UserRegistrationSerializer validates data
   ↓
3. User model creates new user (password hashing)
   ↓
4. User saved to PostgreSQL
   ↓
5. Response sent to client
```

### Movie Search Flow
```
1. Client sends search request with query
   ↓
2. MovieViewSet.search() method called
   ↓
3. Check Redis cache for results
   ↓
4. If not cached:
   a. Call TMDb API
   b. Save movies to PostgreSQL
   c. Cache results in Redis
   ↓
5. Serialize movies
   ↓
6. Return response to client
```

### Authentication Flow
```
1. Client sends credentials
   ↓
2. CustomTokenObtainPairView validates credentials
   ↓
3. Generate JWT tokens (access + refresh)
   ↓
4. Return tokens to client
   ↓
5. Client includes access token in Authorization header
   ↓
6. JWTAuthentication validates token
   ↓
7. Request processed with authenticated user
```

## Database Schema

### Users Table
```
users_user
├── id (PK)
├── username (UNIQUE)
├── email (UNIQUE)
├── password (hashed)
├── first_name
├── last_name
├── bio
├── profile_picture
├── is_staff
├── is_superuser
├── created_at
└── updated_at
```

### Movies Table
```
movies_movie
├── id (PK)
├── tmdb_id (UNIQUE, INDEX)
├── title
├── overview
├── release_date
├── poster_path
├── backdrop_path
├── popularity (INDEX)
├── vote_average (INDEX)
├── vote_count
├── original_language
├── genre_ids (JSON)
├── created_at
└── updated_at
```

### User Favorite Movies Table
```
movies_userfavoritemovie
├── id (PK)
├── user_id (FK, INDEX)
├── movie_id (FK)
├── created_at (INDEX)
└── UNIQUE(user_id, movie_id)
```

### Movie Ratings Table
```
movies_movierating
├── id (PK)
├── user_id (FK, INDEX)
├── movie_id (FK)
├── rating (1-10)
├── review
├── created_at
├── updated_at
└── UNIQUE(user_id, movie_id)
```

## API Endpoint Architecture

### Authentication Endpoints
```
POST   /api/auth/token/              → Obtain JWT token
POST   /api/auth/token/refresh/      → Refresh token
POST   /api/auth/users/              → Register user
GET    /api/auth/users/me/           → Get current user
PUT    /api/auth/users/update_profile/ → Update profile
```

### Movie Endpoints
```
GET    /api/movies/                  → List movies
GET    /api/movies/{id}/             → Get movie details
GET    /api/movies/trending/         → Get trending
GET    /api/movies/popular/          → Get popular
GET    /api/movies/top_rated/        → Get top-rated
GET    /api/movies/search/           → Search movies
GET    /api/movies/{id}/recommendations/ → Get recommendations
```

### Favorite Endpoints
```
POST   /api/movies/{id}/add_to_favorites/    → Add favorite
DELETE /api/movies/{id}/remove_from_favorites/ → Remove favorite
GET    /api/movies/favorites/my_favorites/   → List favorites
```

### Rating Endpoints
```
POST   /api/movies/{id}/rate/        → Create/update rating
DELETE /api/movies/{id}/remove_rating/ → Delete rating
GET    /api/movies/ratings/my_ratings/ → List user ratings
```

## Caching Strategy

### Cache Keys
```
trending_movies_{time_window}_page_{page}
popular_movies_page_{page}
top_rated_movies_page_{page}
search_movies_{query}_page_{page}
movie_details_{movie_id}
recommended_movies_{movie_id}_page_{page}
```

### Cache TTL
```
Default: 15 minutes (900 seconds)
Configurable via CACHE_TTL setting
```

### Cache Invalidation
```
- Automatic expiration after TTL
- Manual invalidation on data updates
- Flush all on deployment
```

## Performance Optimization

### Database Optimization
```python
# Use select_related for foreign keys
movies = Movie.objects.select_related('user')

# Use prefetch_related for reverse relations
users = User.objects.prefetch_related('favorite_movies')

# Add indexes on frequently queried fields
class Meta:
    indexes = [
        models.Index(fields=['tmdb_id']),
        models.Index(fields=['-popularity']),
    ]
```

### Query Optimization
```python
# Limit query results
movies = Movie.objects.all()[:10]

# Use only() to fetch specific fields
movies = Movie.objects.only('id', 'title')

# Use values() for aggregation
ratings = MovieRating.objects.values('movie_id').annotate(
    avg_rating=Avg('rating')
)
```

### API Optimization
```
- Pagination (10 items per page)
- Filtering and searching
- Response compression (gzip)
- CDN for static files
- Rate limiting
```

## Security Architecture

### Authentication
```
1. User credentials → Hash with bcrypt
2. Store hashed password in database
3. On login: Compare hashed passwords
4. Generate JWT tokens (access + refresh)
5. Client includes token in Authorization header
6. Server validates token on each request
```

### Authorization
```
1. Check user is authenticated
2. Check user has required permission
3. Check user owns the resource (if applicable)
4. Allow or deny request
```

### Data Protection
```
- HTTPS/SSL encryption in transit
- Hashed passwords at rest
- Environment variables for secrets
- SQL injection prevention (ORM)
- XSS prevention (serializers)
- CSRF protection (middleware)
```

## Scalability Considerations

### Horizontal Scaling
```
- Multiple Gunicorn workers
- Load balancer (Nginx, HAProxy)
- Database read replicas
- Redis cluster
- Microservices architecture
```

### Vertical Scaling
```
- Increase server resources (CPU, RAM)
- Upgrade database instance
- Increase Redis memory
- Optimize code and queries
```

### Monitoring & Logging
```
- Application logs
- Database query logs
- API access logs
- Error tracking
- Performance monitoring
- Resource utilization
```

## Deployment Architecture

### Development
```
Local machine
├── Django dev server
├── PostgreSQL (local)
└── Redis (local)
```

### Production
```
Cloud provider (AWS, Heroku, etc.)
├── Nginx (reverse proxy)
├── Gunicorn (WSGI server)
├── Django application
├── PostgreSQL (managed)
├── Redis (managed)
└── CDN (static files)
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | Any | Client application |
| Web Server | Nginx | Reverse proxy, load balancing |
| Application | Django 4.2 | Web framework |
| API | DRF 3.14 | REST API development |
| Database | PostgreSQL 15 | Data persistence |
| Cache | Redis 7 | Performance optimization |
| Authentication | JWT | Secure token-based auth |
| Documentation | Swagger/drf-yasg | API documentation |
| Containerization | Docker | Deployment |
| Orchestration | Docker Compose | Multi-container management |

## Future Architecture Enhancements

- [ ] GraphQL API
- [ ] WebSocket support for real-time updates
- [ ] Message queue (Celery + RabbitMQ)
- [ ] Microservices architecture
- [ ] Kubernetes deployment
- [ ] Machine learning recommendations
- [ ] Analytics service
- [ ] Admin dashboard
