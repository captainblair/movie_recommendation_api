"""
Custom decorators for the API.
"""

from functools import wraps
from django.core.cache import cache
from django.utils.decorators import decorator_from_middleware_with_args
import logging

logger = logging.getLogger(__name__)


def cache_response(timeout=None):
    """
    Decorator to cache view responses.
    
    Args:
        timeout: Cache timeout in seconds. If None, uses CACHE_TTL from settings.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            from django.conf import settings
            
            # Generate cache key from request path and query params
            cache_key = f"view_{request.path}_{request.GET.urlencode()}"
            
            # Try to get from cache
            cached_response = cache.get(cache_key)
            if cached_response:
                logger.info(f"Cache hit for {cache_key}")
                return cached_response
            
            # Call the view function
            response = view_func(request, *args, **kwargs)
            
            # Cache the response
            cache_timeout = timeout or settings.CACHE_TTL
            cache.set(cache_key, response, cache_timeout)
            logger.info(f"Cached response for {cache_key} with timeout {cache_timeout}s")
            
            return response
        
        return wrapper
    return decorator


def handle_exceptions(view_func):
    """
    Decorator to handle common exceptions in views.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {view_func.__name__}: {str(e)}")
            raise
    
    return wrapper


def require_api_key(view_func):
    """
    Decorator to require API key for view access.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        api_key = request.META.get('HTTP_X_API_KEY')
        if not api_key:
            from rest_framework.response import Response
            from rest_framework import status
            return Response(
                {'error': 'API key is required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)
    
    return wrapper
