# Security Policy

## Reporting Security Vulnerabilities

If you discover a security vulnerability in the Movie Recommendation API, please **do not** open a public GitHub issue. Instead, please email security@example.com with the following information:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will acknowledge receipt of your report within 48 hours and will provide an estimated timeline for a fix.

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip list --outdated
   pip install --upgrade package-name
   ```

2. **Use Strong Passwords**
   - Minimum 8 characters
   - Mix of uppercase, lowercase, numbers, and special characters
   - Avoid common words and personal information

3. **Protect API Keys**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys regularly
   - Use different keys for different environments

4. **Enable HTTPS**
   - Always use HTTPS in production
   - Use valid SSL certificates
   - Enable HSTS headers

5. **Monitor Access**
   - Review access logs regularly
   - Set up alerts for suspicious activity
   - Use rate limiting to prevent abuse

### For Developers

1. **Input Validation**
   ```python
   # Always validate user input
   from rest_framework import serializers
   
   class MovieSerializer(serializers.Serializer):
       title = serializers.CharField(max_length=255)
       rating = serializers.IntegerField(min_value=1, max_value=10)
   ```

2. **SQL Injection Prevention**
   ```python
   # Use ORM instead of raw SQL
   # Good
   movies = Movie.objects.filter(title__icontains=query)
   
   # Bad
   movies = Movie.objects.raw(f"SELECT * FROM movies WHERE title LIKE '%{query}%'")
   ```

3. **Cross-Site Scripting (XSS) Prevention**
   ```python
   # Django templates automatically escape output
   # {{ user_input }}  # Automatically escaped
   
   # For JSON responses, use serializers
   serializer = MovieSerializer(movie)
   return Response(serializer.data)
   ```

4. **Cross-Site Request Forgery (CSRF) Protection**
   ```python
   # Django includes CSRF middleware by default
   # Include CSRF token in POST requests
   ```

5. **Authentication & Authorization**
   ```python
   # Use JWT for API authentication
   from rest_framework_simplejwt.authentication import JWTAuthentication
   
   class MovieViewSet(viewsets.ModelViewSet):
       authentication_classes = [JWTAuthentication]
       permission_classes = [IsAuthenticated]
   ```

6. **Secure Password Storage**
   ```python
   # Django automatically hashes passwords
   user = User.objects.create_user(
       username='user',
       password='password'  # Automatically hashed
   )
   ```

7. **Environment Variables**
   ```python
   # Never hardcode sensitive data
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   SECRET_KEY = os.getenv('SECRET_KEY')
   ```

8. **Error Handling**
   ```python
   # Don't expose sensitive information in error messages
   # Good
   return Response({'error': 'Invalid credentials'}, status=401)
   
   # Bad
   return Response({'error': f'User {username} not found'}, status=401)
   ```

## Security Headers

Configure these headers in production:

```python
# config/settings/production.py

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## Dependency Security

### Regular Updates

```bash
# Check for outdated packages
pip list --outdated

# Check for security vulnerabilities
pip install safety
safety check

# Update all packages
pip install --upgrade -r requirements.txt
```

### Dependency Scanning

Use tools like:
- [Safety](https://safety.readthedocs.io/)
- [Bandit](https://bandit.readthedocs.io/)
- [OWASP Dependency-Check](https://owasp.org/www-project-dependency-check/)

## Database Security

1. **Use Strong Credentials**
   ```env
   POSTGRES_USER=secure_username
   POSTGRES_PASSWORD=very-secure-password
   ```

2. **Restrict Access**
   ```bash
   # Only allow local connections
   # Edit /etc/postgresql/postgresql.conf
   listen_addresses = 'localhost'
   ```

3. **Enable SSL**
   ```python
   # config/settings/production.py
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'SSLMODE': 'require',
           ...
       }
   }
   ```

4. **Regular Backups**
   ```bash
   # Automated daily backups
   pg_dump movie_db > backup_$(date +%Y%m%d).sql
   ```

## API Security

1. **Rate Limiting**
   ```python
   # Implement rate limiting
   from rest_framework.throttling import UserRateThrottle
   
   class UserRateThrottle(UserRateThrottle):
       scope = 'user'
       THROTTLE_RATES = {
           'user': '1000/hour'
       }
   ```

2. **API Key Management**
   - Rotate keys regularly
   - Use different keys for different environments
   - Monitor key usage
   - Revoke compromised keys immediately

3. **CORS Configuration**
   ```python
   # Only allow trusted origins
   CORS_ALLOWED_ORIGINS = [
       "https://yourdomain.com",
       "https://www.yourdomain.com",
   ]
   ```

## Logging & Monitoring

1. **Enable Logging**
   ```python
   # Log security events
   import logging
   logger = logging.getLogger('security')
   logger.warning(f'Failed login attempt for user {username}')
   ```

2. **Monitor for Suspicious Activity**
   - Failed login attempts
   - Unusual API usage patterns
   - Rate limit violations
   - Database errors

3. **Set Up Alerts**
   - High error rates
   - Unusual traffic patterns
   - Failed authentication attempts
   - Resource exhaustion

## Incident Response

If a security incident occurs:

1. **Assess the Situation**
   - Determine the scope of the breach
   - Identify affected users/data
   - Evaluate the severity

2. **Contain the Incident**
   - Revoke compromised credentials
   - Block suspicious IP addresses
   - Disable affected accounts if necessary

3. **Investigate**
   - Review logs
   - Identify root cause
   - Document findings

4. **Notify Users**
   - Inform affected users
   - Provide remediation steps
   - Offer support

5. **Remediate**
   - Fix the vulnerability
   - Deploy patches
   - Update security measures

6. **Post-Incident Review**
   - Analyze what happened
   - Identify improvements
   - Update security policies

## Compliance

### OWASP Top 10

The API is designed to mitigate common vulnerabilities:

1. **Injection** - Input validation and parameterized queries
2. **Broken Authentication** - JWT with secure token management
3. **Sensitive Data Exposure** - HTTPS, encryption at rest
4. **XML External Entities (XXE)** - Not applicable (JSON API)
5. **Broken Access Control** - Permission classes and authentication
6. **Security Misconfiguration** - Security headers, secure defaults
7. **Cross-Site Scripting (XSS)** - Template escaping, serializers
8. **Insecure Deserialization** - Input validation
9. **Using Components with Known Vulnerabilities** - Regular updates
10. **Insufficient Logging & Monitoring** - Comprehensive logging

### GDPR Compliance

- User data is stored securely
- Users can request data deletion
- Privacy policy should be provided
- Data processing agreements in place

## Security Testing

### Manual Testing

```bash
# Test for common vulnerabilities
# SQL Injection
curl "http://localhost:8000/api/movies/search/?q='; DROP TABLE movies; --"

# XSS
curl "http://localhost:8000/api/movies/search/?q=<script>alert('xss')</script>"

# CSRF
# Test CSRF protection on POST requests
```

### Automated Testing

```bash
# Run security checks
python manage.py check --deploy

# Use Bandit for code analysis
bandit -r .

# Use Safety for dependency scanning
safety check
```

## Third-Party Security

- **TMDb API**: Use API key securely, monitor usage
- **PostgreSQL**: Keep updated, use strong credentials
- **Redis**: Secure with password, restrict access
- **Django**: Keep updated to latest security patches

## Contact

For security issues, contact: security@example.com

For general inquiries, visit: https://github.com/your-username/movie_recommendation_api
