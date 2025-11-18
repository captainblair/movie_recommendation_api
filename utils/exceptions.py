"""
Custom exceptions for the API.
"""

from rest_framework.exceptions import APIException
from rest_framework import status


class TMDbAPIException(APIException):
    """Exception raised when TMDb API request fails."""
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = 'Failed to fetch data from TMDb API.'
    default_code = 'tmdb_api_error'


class InvalidMovieException(APIException):
    """Exception raised when movie data is invalid."""
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid movie data.'
    default_code = 'invalid_movie'


class MovieNotFound(APIException):
    """Exception raised when movie is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Movie not found.'
    default_code = 'movie_not_found'


class UserNotFound(APIException):
    """Exception raised when user is not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'User not found.'
    default_code = 'user_not_found'


class CacheException(APIException):
    """Exception raised when cache operation fails."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Cache operation failed.'
    default_code = 'cache_error'
