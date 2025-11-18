# Contributing to Movie Recommendation API

Thank you for your interest in contributing to the Movie Recommendation API! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome diverse perspectives
- Focus on constructive feedback
- Report inappropriate behavior

## Getting Started

### 1. Fork the Repository
```bash
git clone https://github.com/your-username/movie_recommendation_api.git
cd movie_recommendation_api
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Create Environment File
```bash
cp .env.example .env
```

## Development Workflow

### Writing Code

1. **Follow PEP 8 style guide**
```python
# Good
def get_trending_movies(time_window='week'):
    """Get trending movies from TMDb API."""
    pass

# Bad
def getTrendingMovies(timeWindow='week'):
    pass
```

2. **Add docstrings to functions and classes**
```python
def search_movies(query, page=1):
    """
    Search for movies by title.
    
    Args:
        query: Search query string
        page: Page number for pagination
    
    Returns:
        List of movies matching the query
    
    Raises:
        TMDbAPIException: If API request fails
    """
    pass
```

3. **Use type hints**
```python
from typing import List, Optional

def get_movies(limit: int = 10) -> List[Movie]:
    """Get a list of movies."""
    pass
```

4. **Write meaningful variable names**
```python
# Good
user_favorite_movies = UserFavoriteMovie.objects.filter(user=user)

# Bad
ufm = UserFavoriteMovie.objects.filter(user=user)
```

### Testing

1. **Write tests for new features**
```python
class MovieAPITestCase(TestCase):
    def test_trending_movies_endpoint(self):
        """Test trending movies endpoint returns 200."""
        response = self.client.get('/api/movies/trending/')
        self.assertEqual(response.status_code, 200)
```

2. **Run tests before committing**
```bash
python manage.py test
```

3. **Check test coverage**
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

### Linting and Formatting

1. **Install linting tools**
```bash
pip install flake8 black isort
```

2. **Format code**
```bash
black .
isort .
```

3. **Check for issues**
```bash
flake8 .
```

## Git Workflow

### Commit Messages

Follow conventional commits format:

```
feat: add trending movies endpoint
fix: resolve cache invalidation issue
docs: update API documentation
test: add tests for user authentication
perf: optimize database queries
refactor: restructure movie serializers
```

### Commit Guidelines

- Make small, focused commits
- Write descriptive commit messages
- Reference issues in commits: `Fixes #123`

### Example Commit

```bash
git add .
git commit -m "feat: implement movie recommendations endpoint

- Add recommendations endpoint to MovieViewSet
- Integrate TMDb recommendations API
- Add caching for recommendations
- Add tests for recommendations

Fixes #45"
```

## Pull Request Process

### 1. Before Creating PR

- Ensure all tests pass
- Update documentation if needed
- Add tests for new features
- Follow code style guidelines

### 2. Create Pull Request

**Title:** Use conventional commits format
```
feat: add movie search functionality
```

**Description:**
```markdown
## Description
Add search functionality to find movies by title.

## Changes
- Add search endpoint to MovieViewSet
- Integrate TMDb search API
- Add caching for search results
- Add comprehensive tests

## Related Issues
Fixes #123

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [x] Code follows style guidelines
- [x] Documentation updated
- [x] Tests added/updated
- [x] No breaking changes
```

### 3. Code Review

- Address feedback promptly
- Ask for clarification if needed
- Make requested changes in new commits
- Request re-review after changes

### 4. Merge

Once approved, your PR will be merged to main branch.

## Reporting Issues

### Bug Reports

**Title:** Clear and descriptive
```
User authentication fails with special characters in password
```

**Description:**
```markdown
## Description
Brief description of the bug

## Steps to Reproduce
1. Create user with password containing special characters
2. Try to login
3. Observe error

## Expected Behavior
User should be able to login successfully

## Actual Behavior
Login fails with validation error

## Environment
- OS: Windows 10
- Python: 3.11
- Django: 4.2.7

## Screenshots
[If applicable]

## Additional Context
[Any other relevant information]
```

### Feature Requests

**Title:** Clear and descriptive
```
Add email notifications for favorite movies
```

**Description:**
```markdown
## Description
Users should receive email notifications when new movies are added to their favorite genres.

## Motivation
This feature would improve user engagement and keep users informed about new content.

## Proposed Solution
- Add email notification settings to user profile
- Create background task to check for new movies
- Send daily/weekly digest emails

## Alternatives
- In-app notifications instead of email
- Push notifications

## Additional Context
[Any other relevant information]
```

## Documentation

### Updating Documentation

1. **API Documentation** (`docs/API_DOCUMENTATION.md`)
   - Document new endpoints
   - Include request/response examples
   - Update error codes

2. **README** (`README.md`)
   - Update feature list
   - Update setup instructions
   - Add new sections if needed

3. **Code Comments**
   - Explain complex logic
   - Document edge cases
   - Add examples where helpful

### Documentation Style

```python
def complex_function(param1: str, param2: int) -> dict:
    """
    Brief description of what the function does.
    
    Longer description explaining the function's purpose,
    behavior, and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param2 is negative
        TypeError: When param1 is not a string
    
    Example:
        >>> result = complex_function("test", 10)
        >>> print(result)
        {'status': 'success'}
    """
    pass
```

## Performance Considerations

### Database Queries

- Use `select_related()` for foreign keys
- Use `prefetch_related()` for reverse relations
- Add database indexes for frequently queried fields
- Avoid N+1 queries

```python
# Good
movies = Movie.objects.select_related('user').all()

# Bad
movies = Movie.objects.all()
for movie in movies:
    print(movie.user.username)  # N+1 query
```

### Caching

- Cache expensive operations
- Use appropriate cache TTL
- Invalidate cache when data changes

```python
from django.core.cache import cache

def get_trending_movies():
    cache_key = 'trending_movies'
    cached = cache.get(cache_key)
    if cached:
        return cached
    
    movies = Movie.objects.filter(trending=True)
    cache.set(cache_key, movies, 3600)  # 1 hour
    return movies
```

## Security Guidelines

- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Validate and sanitize user input
- Use parameterized queries
- Keep dependencies updated
- Report security vulnerabilities privately

## Questions?

- Open an issue with the `question` label
- Check existing issues and discussions
- Contact maintainers directly

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
