"""
TMDb API Client for fetching movie data.
"""
import requests
import logging
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class TMDbClient:
    """Client for interacting with The Movie Database (TMDb) API."""
    
    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.base_url = settings.TMDB_BASE_URL
        self.timeout = 10
    
    def _make_request(self, endpoint, params=None):
        """
        Make a request to TMDb API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
        
        Returns:
            Response data or None if request fails
        """
        if not self.api_key:
            logger.error("TMDB_API_KEY not configured")
            return None
        
        if params is None:
            params = {}
        
        params['api_key'] = self.api_key
        
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDb API request failed: {str(e)}")
            return None
    
    def get_trending_movies(self, time_window='week', page=1):
        """
        Get trending movies.
        
        Args:
            time_window: 'day' or 'week'
            page: Page number for pagination
        
        Returns:
            List of trending movies
        """
        cache_key = f"trending_movies_{time_window}_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached trending movies for {time_window}")
            return cached_data
        
        endpoint = f"/trending/movie/{time_window}"
        params = {'page': page}
        
        data = self._make_request(endpoint, params)
        
        if data:
            cache.set(cache_key, data, settings.CACHE_TTL)
            return data
        
        return None
    
    def get_recommended_movies(self, movie_id, page=1):
        """
        Get recommended movies based on a specific movie.
        
        Args:
            movie_id: TMDb movie ID
            page: Page number for pagination
        
        Returns:
            List of recommended movies
        """
        cache_key = f"recommended_movies_{movie_id}_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached recommendations for movie {movie_id}")
            return cached_data
        
        endpoint = f"/movie/{movie_id}/recommendations"
        params = {'page': page}
        
        data = self._make_request(endpoint, params)
        
        if data:
            cache.set(cache_key, data, settings.CACHE_TTL)
            return data
        
        return None
    
    def get_movie_details(self, movie_id):
        """
        Get detailed information about a specific movie.
        
        Args:
            movie_id: TMDb movie ID
        
        Returns:
            Movie details
        """
        cache_key = f"movie_details_{movie_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached details for movie {movie_id}")
            return cached_data
        
        endpoint = f"/movie/{movie_id}"
        
        data = self._make_request(endpoint)
        
        if data:
            cache.set(cache_key, data, settings.CACHE_TTL)
            return data
        
        return None
    
    def search_movies(self, query, page=1):
        """
        Search for movies by title.
        
        Args:
            query: Search query
            page: Page number for pagination
        
        Returns:
            Search results
        """
        cache_key = f"search_movies_{query}_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached search results for '{query}'")
            return cached_data
        
        endpoint = "/search/movie"
        params = {'query': query, 'page': page}
        
        data = self._make_request(endpoint, params)
        
        if data:
            cache.set(cache_key, data, settings.CACHE_TTL)
            return data
        
        return None
    
    def get_popular_movies(self, page=1):
        """
        Get popular movies.
        
        Args:
            page: Page number for pagination
        
        Returns:
            List of popular movies
        """
        cache_key = f"popular_movies_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached popular movies")
            return cached_data
        
        endpoint = "/movie/popular"
        params = {'page': page}
        
        data = self._make_request(endpoint, params)
        
        if data:
            cache.set(cache_key, data, settings.CACHE_TTL)
            return data
        
        return None
    
    def get_top_rated_movies(self, page=1):
        """
        Get top-rated movies.
        
        Args:
            page: Page number for pagination
        
        Returns:
            List of top-rated movies
        """
        cache_key = f"top_rated_movies_page_{page}"
        cached_data = cache.get(cache_key)
        
        if cached_data:
            logger.info(f"Returning cached top-rated movies")
            return cached_data
        
        endpoint = "/movie/top_rated"
        params = {'page': page}
        
        data = self._make_request(endpoint, params)
        
        if data:
            cache.set(cache_key, data, settings.CACHE_TTL)
            return data
        
        return None
