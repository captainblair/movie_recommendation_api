"""
Management command to fetch trending movies from TMDb API.
"""

from django.core.management.base import BaseCommand
from apps.movies.models import Movie
from apps.movies.tmdb_client import TMDbClient
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch trending movies from TMDb API and save to database'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--time-window',
            type=str,
            default='week',
            choices=['day', 'week'],
            help='Time window for trending movies (day or week)'
        )
        parser.add_argument(
            '--pages',
            type=int,
            default=1,
            help='Number of pages to fetch'
        )
    
    def handle(self, *args, **options):
        time_window = options['time_window']
        pages = options['pages']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Fetching trending movies for {time_window}...'
            )
        )
        
        tmdb_client = TMDbClient()
        movies_created = 0
        movies_updated = 0
        
        for page in range(1, pages + 1):
            data = tmdb_client.get_trending_movies(time_window, page)
            
            if not data:
                self.stdout.write(
                    self.style.ERROR(f'Failed to fetch page {page}')
                )
                continue
            
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
                
                if created:
                    movies_created += 1
                else:
                    movies_updated += 1
                    # Update existing movie
                    movie.popularity = movie_data.get('popularity', 0)
                    movie.vote_average = movie_data.get('vote_average', 0)
                    movie.vote_count = movie_data.get('vote_count', 0)
                    movie.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully fetched {pages} pages. '
                f'Created: {movies_created}, Updated: {movies_updated}'
            )
        )
