# API Documentation

## Base URL
```
http://localhost:8000/api
```

## Authentication

All endpoints except authentication and public movie endpoints require JWT authentication.

### Obtaining a Token

**Endpoint:** `POST /auth/token/`

**Request:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
  }
}
```

### Refreshing a Token

**Endpoint:** `POST /auth/token/refresh/`

**Request:**
```json
{
  "refresh": "your_refresh_token"
}
```

**Response:**
```json
{
  "access": "new_access_token"
}
```

## User Endpoints

### Register a New User

**Endpoint:** `POST /auth/users/`

**Request:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": null,
    "profile_picture": null,
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

### Get Current User Profile

**Endpoint:** `GET /auth/users/me/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Response:**
```json
{
  "id": 1,
  "username": "newuser",
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Movie enthusiast",
  "profile_picture": "https://...",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update User Profile

**Endpoint:** `PUT /auth/users/update_profile/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Request:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "bio": "Updated bio"
}
```

**Response:**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "newuser",
    "email": "newuser@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "bio": "Updated bio",
    "profile_picture": null,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  }
}
```

## Movie Endpoints

### List All Movies

**Endpoint:** `GET /movies/`

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Number of results per page (default: 10, max: 100)

**Response:**
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/movies/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "tmdb_id": 550,
      "title": "Fight Club",
      "overview": "An insomniac office worker...",
      "release_date": "1999-10-15",
      "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
      "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
      "backdrop_path": "/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
      "backdrop_url": "https://image.tmdb.org/t/p/w1280/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
      "popularity": 26.5,
      "vote_average": 8.4,
      "vote_count": 15000,
      "original_language": "en",
      "genre_ids": [28, 18],
      "is_favorite": false,
      "user_rating": null,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Get Trending Movies

**Endpoint:** `GET /movies/trending/`

**Query Parameters:**
- `time_window`: 'day' or 'week' (default: 'week')
- `page`: Page number (default: 1)

**Response:** Same as list all movies

### Get Popular Movies

**Endpoint:** `GET /movies/popular/`

**Query Parameters:**
- `page`: Page number (default: 1)

**Response:** Same as list all movies

### Get Top-Rated Movies

**Endpoint:** `GET /movies/top_rated/`

**Query Parameters:**
- `page`: Page number (default: 1)

**Response:** Same as list all movies

### Search Movies

**Endpoint:** `GET /movies/search/`

**Query Parameters:**
- `q`: Search query (required)
- `page`: Page number (default: 1)

**Example:**
```
GET /movies/search/?q=fight&page=1
```

**Response:** Same as list all movies

### Get Movie Details

**Endpoint:** `GET /movies/{id}/`

**Response:**
```json
{
  "id": 1,
  "tmdb_id": 550,
  "title": "Fight Club",
  "overview": "An insomniac office worker and a devil-may-care soapmaker...",
  "release_date": "1999-10-15",
  "poster_path": "/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "poster_url": "https://image.tmdb.org/t/p/w500/pB8BM7pdSp6B6Ih7QZ4DrQ3PmJK.jpg",
  "backdrop_path": "/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
  "backdrop_url": "https://image.tmdb.org/t/p/w1280/rr7E0NoGKxvbkb89eR1GwfoYjpA.jpg",
  "popularity": 26.5,
  "vote_average": 8.4,
  "vote_count": 15000,
  "original_language": "en",
  "genre_ids": [28, 18],
  "is_favorite": false,
  "user_rating": null,
  "average_rating": 8.2,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Get Movie Recommendations

**Endpoint:** `GET /movies/{id}/recommendations/`

**Query Parameters:**
- `page`: Page number (default: 1)

**Response:** Same as list all movies

## Favorite Movies Endpoints

### Add Movie to Favorites

**Endpoint:** `POST /movies/{id}/add_to_favorites/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Response:**
```json
{
  "message": "Movie added to favorites"
}
```

### Remove Movie from Favorites

**Endpoint:** `DELETE /movies/{id}/remove_from_favorites/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Response:**
```json
{
  "message": "Movie removed from favorites"
}
```

### Get User's Favorite Movies

**Endpoint:** `GET /movies/favorites/my_favorites/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Number of results per page (default: 10)

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "movie": {
        "id": 1,
        "tmdb_id": 550,
        "title": "Fight Club",
        ...
      },
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Movie Ratings Endpoints

### Rate a Movie

**Endpoint:** `POST /movies/{id}/rate/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Request:**
```json
{
  "rating": 9,
  "review": "Amazing movie! Highly recommended."
}
```

**Response:**
```json
{
  "id": 1,
  "movie": {
    "id": 1,
    "tmdb_id": 550,
    "title": "Fight Club",
    ...
  },
  "rating": 9,
  "review": "Amazing movie! Highly recommended.",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Update Movie Rating

**Endpoint:** `PUT /movies/{id}/rate/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Request:**
```json
{
  "rating": 8,
  "review": "Updated review"
}
```

**Response:** Same as rate a movie

### Remove Movie Rating

**Endpoint:** `DELETE /movies/{id}/remove_rating/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Response:**
```json
{
  "message": "Rating removed"
}
```

### Get User's Movie Ratings

**Endpoint:** `GET /movies/ratings/my_ratings/`

**Headers:**
```
Authorization: Bearer your_access_token
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Number of results per page (default: 10)

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "movie": {
        "id": 1,
        "tmdb_id": 550,
        "title": "Fight Club",
        ...
      },
      "rating": 9,
      "review": "Amazing movie!",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request data",
  "details": {
    "field_name": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error."
}
```

## Rate Limiting

API endpoints are rate-limited to prevent abuse. The rate limit is:
- **Authenticated users:** 1000 requests per hour
- **Anonymous users:** 100 requests per hour

Rate limit information is included in response headers:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1234567890
```

## Pagination

List endpoints support pagination with the following parameters:
- `page`: Page number (default: 1)
- `page_size`: Number of results per page (default: 10, max: 100)

Example:
```
GET /movies/?page=2&page_size=20
```

## Filtering and Searching

Search endpoints support filtering by various fields:
- `q`: Search query (for search endpoint)
- `title`: Movie title
- `release_year`: Release year
- `min_rating`: Minimum rating
- `max_rating`: Maximum rating
- `min_popularity`: Minimum popularity

Example:
```
GET /movies/search/?q=fight&min_rating=7&release_year=1999
```

## Caching

The API implements Redis caching for improved performance:
- Trending movies: Cached for 15 minutes
- Popular movies: Cached for 15 minutes
- Top-rated movies: Cached for 15 minutes
- Search results: Cached for 15 minutes
- Movie details: Cached for 15 minutes
- Recommendations: Cached for 15 minutes

Cache is automatically invalidated when data is updated.
