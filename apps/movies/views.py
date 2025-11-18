from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q
import logging

from .models import Movie, UserFavoriteMovie, MovieRating
from .serializers import (
    MovieSerializer,
    MovieDetailSerializer,
    UserFavoriteMovieSerializer,
    MovieRatingSerializer,
    MovieRatingCreateSerializer
)
from .tmdb_client import TMDbClient

logger = logging.getLogger(__name__)


class MoviePagination(PageNumberPagination):
    """Custom pagination for movies."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class MovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for movie management.
    
    Provides endpoints for:
    - Trending movies
    - Recommended movies
    - Popular movies
    - Top-rated movies
    - Movie search
    - Movie details
    - User favorite movies
    - Movie ratings
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Override permissions based on action."""
        if self.action in ['list', 'retrieve', 'trending', 'popular', 'top_rated', 'search']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'retrieve':
            return MovieDetailSerializer
        return MovieSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def trending(self, request):
        """
        Get trending movies.
        
        Query parameters:
        - time_window: 'day' or 'week' (default: 'week')
        - page: Page number (default: 1)
        """
        time_window = request.query_params.get('time_window', 'week')
        page = request.query_params.get('page', 1)
        
        if time_window not in ['day', 'week']:
            return Response(
                {'error': "time_window must be 'day' or 'week'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tmdb_client = TMDbClient()
        data = tmdb_client.get_trending_movies(time_window, page)
        
        if not data:
            return Response(
                {'error': 'Failed to fetch trending movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Save movies to database
        movies = []
        for movie_data in data.get('results', []):
            movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data.get('title', ''),
                    'overview': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date'),
                    'poster_path': movie_data.get('poster_path'),
                    'backdrop_path': movie_data.get('backdrop_path'),
                    'popularity': movie_data.get('popularity', 0),
                    'vote_average': movie_data.get('vote_average', 0),
                    'vote_count': movie_data.get('vote_count', 0),
                    'original_language': movie_data.get('original_language'),
                    'genre_ids': movie_data.get('genre_ids', []),
                }
            )
            movies.append(movie)
        
        serializer = self.get_serializer(movies, many=True, context={'request': request})
        return Response({
            'count': data.get('total_results', 0),
            'page': data.get('page', 1),
            'total_pages': data.get('total_pages', 1),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def popular(self, request):
        """Get popular movies."""
        page = request.query_params.get('page', 1)
        
        tmdb_client = TMDbClient()
        data = tmdb_client.get_popular_movies(page)
        
        if not data:
            return Response(
                {'error': 'Failed to fetch popular movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Save movies to database
        movies = []
        for movie_data in data.get('results', []):
            movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data.get('title', ''),
                    'overview': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date'),
                    'poster_path': movie_data.get('poster_path'),
                    'backdrop_path': movie_data.get('backdrop_path'),
                    'popularity': movie_data.get('popularity', 0),
                    'vote_average': movie_data.get('vote_average', 0),
                    'vote_count': movie_data.get('vote_count', 0),
                    'original_language': movie_data.get('original_language'),
                    'genre_ids': movie_data.get('genre_ids', []),
                }
            )
            movies.append(movie)
        
        serializer = self.get_serializer(movies, many=True, context={'request': request})
        return Response({
            'count': data.get('total_results', 0),
            'page': data.get('page', 1),
            'total_pages': data.get('total_pages', 1),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def top_rated(self, request):
        """Get top-rated movies."""
        page = request.query_params.get('page', 1)
        
        tmdb_client = TMDbClient()
        data = tmdb_client.get_top_rated_movies(page)
        
        if not data:
            return Response(
                {'error': 'Failed to fetch top-rated movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Save movies to database
        movies = []
        for movie_data in data.get('results', []):
            movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data.get('title', ''),
                    'overview': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date'),
                    'poster_path': movie_data.get('poster_path'),
                    'backdrop_path': movie_data.get('backdrop_path'),
                    'popularity': movie_data.get('popularity', 0),
                    'vote_average': movie_data.get('vote_average', 0),
                    'vote_count': movie_data.get('vote_count', 0),
                    'original_language': movie_data.get('original_language'),
                    'genre_ids': movie_data.get('genre_ids', []),
                }
            )
            movies.append(movie)
        
        serializer = self.get_serializer(movies, many=True, context={'request': request})
        return Response({
            'count': data.get('total_results', 0),
            'page': data.get('page', 1),
            'total_pages': data.get('total_pages', 1),
            'results': serializer.data
        })
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request):
        """Search for movies by title."""
        query = request.query_params.get('q', '')
        page = request.query_params.get('page', 1)
        
        if not query:
            return Response(
                {'error': 'Search query is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tmdb_client = TMDbClient()
        data = tmdb_client.search_movies(query, page)
        
        if not data:
            return Response(
                {'error': 'Failed to search movies'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Save movies to database
        movies = []
        for movie_data in data.get('results', []):
            if 'id' in movie_data:
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=movie_data['id'],
                    defaults={
                        'title': movie_data.get('title', ''),
                        'overview': movie_data.get('overview', ''),
                        'release_date': movie_data.get('release_date'),
                        'poster_path': movie_data.get('poster_path'),
                        'backdrop_path': movie_data.get('backdrop_path'),
                        'popularity': movie_data.get('popularity', 0),
                        'vote_average': movie_data.get('vote_average', 0),
                        'vote_count': movie_data.get('vote_count', 0),
                        'original_language': movie_data.get('original_language'),
                        'genre_ids': movie_data.get('genre_ids', []),
                    }
                )
                movies.append(movie)
        
        serializer = self.get_serializer(movies, many=True, context={'request': request})
        return Response({
            'count': data.get('total_results', 0),
            'page': data.get('page', 1),
            'total_pages': data.get('total_pages', 1),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def recommendations(self, request, pk=None):
        """Get recommendations based on a specific movie."""
        movie = self.get_object()
        page = request.query_params.get('page', 1)
        
        tmdb_client = TMDbClient()
        data = tmdb_client.get_recommended_movies(movie.tmdb_id, page)
        
        if not data:
            return Response(
                {'error': 'Failed to fetch recommendations'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        
        # Save movies to database
        movies = []
        for movie_data in data.get('results', []):
            recommended_movie, created = Movie.objects.get_or_create(
                tmdb_id=movie_data['id'],
                defaults={
                    'title': movie_data.get('title', ''),
                    'overview': movie_data.get('overview', ''),
                    'release_date': movie_data.get('release_date'),
                    'poster_path': movie_data.get('poster_path'),
                    'backdrop_path': movie_data.get('backdrop_path'),
                    'popularity': movie_data.get('popularity', 0),
                    'vote_average': movie_data.get('vote_average', 0),
                    'vote_count': movie_data.get('vote_count', 0),
                    'original_language': movie_data.get('original_language'),
                    'genre_ids': movie_data.get('genre_ids', []),
                }
            )
            movies.append(recommended_movie)
        
        serializer = self.get_serializer(movies, many=True, context={'request': request})
        return Response({
            'count': data.get('total_results', 0),
            'page': data.get('page', 1),
            'total_pages': data.get('total_pages', 1),
            'results': serializer.data
        })
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_favorites(self, request, pk=None):
        """Add a movie to user's favorites."""
        movie = self.get_object()
        
        favorite, created = UserFavoriteMovie.objects.get_or_create(
            user=request.user,
            movie=movie
        )
        
        if created:
            return Response(
                {'message': 'Movie added to favorites'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'message': 'Movie is already in favorites'},
                status=status.HTTP_200_OK
            )
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_from_favorites(self, request, pk=None):
        """Remove a movie from user's favorites."""
        movie = self.get_object()
        
        try:
            favorite = UserFavoriteMovie.objects.get(user=request.user, movie=movie)
            favorite.delete()
            return Response(
                {'message': 'Movie removed from favorites'},
                status=status.HTTP_204_NO_CONTENT
            )
        except UserFavoriteMovie.DoesNotExist:
            return Response(
                {'error': 'Movie is not in favorites'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post', 'put', 'patch'], permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        """Rate a movie."""
        movie = self.get_object()
        serializer = MovieRatingCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        rating, created = MovieRating.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults=serializer.validated_data
        )
        
        response_serializer = MovieRatingSerializer(rating)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        
        return Response(response_serializer.data, status=status_code)
    
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_rating(self, request, pk=None):
        """Remove rating from a movie."""
        movie = self.get_object()
        
        try:
            rating = MovieRating.objects.get(user=request.user, movie=movie)
            rating.delete()
            return Response(
                {'message': 'Rating removed'},
                status=status.HTTP_204_NO_CONTENT
            )
        except MovieRating.DoesNotExist:
            return Response(
                {'error': 'No rating found for this movie'},
                status=status.HTTP_404_NOT_FOUND
            )


class FavoriteMovieViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user's favorite movies.
    """
    serializer_class = UserFavoriteMovieSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """Return favorite movies for the current user."""
        return UserFavoriteMovie.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_favorites(self, request):
        """Get current user's favorite movies."""
        favorites = self.get_queryset()
        page = self.paginate_queryset(favorites)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)


class MovieRatingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing movie ratings.
    """
    serializer_class = MovieRatingSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MoviePagination
    
    def get_queryset(self):
        """Return ratings for the current user."""
        return MovieRating.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_ratings(self, request):
        """Get current user's movie ratings."""
        ratings = self.get_queryset()
        page = self.paginate_queryset(ratings)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(ratings, many=True)
        return Response(serializer.data)
