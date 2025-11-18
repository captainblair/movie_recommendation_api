from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Movie, UserFavoriteMovie, MovieRating

User = get_user_model()


class MovieAPITestCase(TestCase):
    """Test cases for Movie API."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            tmdb_id=550,
            title='Fight Club',
            overview='An insomniac office worker and a devil-may-care soapmaker form an underground fight club.',
            release_date='1999-10-15',
            popularity=26.5,
            vote_average=8.4,
            vote_count=15000
        )
    
    def test_trending_movies(self):
        """Test trending movies endpoint."""
        response = self.client.get('/api/movies/trending/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_popular_movies(self):
        """Test popular movies endpoint."""
        response = self.client.get('/api/movies/popular/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_top_rated_movies(self):
        """Test top-rated movies endpoint."""
        response = self.client.get('/api/movies/top_rated/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_search_movies(self):
        """Test search movies endpoint."""
        response = self.client.get('/api/movies/search/?q=fight')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_movie_detail(self):
        """Test movie detail endpoint."""
        response = self.client.get(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Fight Club')


class FavoriteMovieTestCase(TestCase):
    """Test cases for favorite movies."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            tmdb_id=550,
            title='Fight Club',
            overview='An insomniac office worker and a devil-may-care soapmaker form an underground fight club.',
            release_date='1999-10-15',
            popularity=26.5,
            vote_average=8.4,
            vote_count=15000
        )
        self.client.force_authenticate(user=self.user)
    
    def test_add_to_favorites(self):
        """Test adding movie to favorites."""
        response = self.client.post(f'/api/movies/{self.movie.id}/add_to_favorites/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserFavoriteMovie.objects.filter(user=self.user, movie=self.movie).exists())
    
    def test_remove_from_favorites(self):
        """Test removing movie from favorites."""
        UserFavoriteMovie.objects.create(user=self.user, movie=self.movie)
        response = self.client.delete(f'/api/movies/{self.movie.id}/remove_from_favorites/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserFavoriteMovie.objects.filter(user=self.user, movie=self.movie).exists())


class MovieRatingTestCase(TestCase):
    """Test cases for movie ratings."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.movie = Movie.objects.create(
            tmdb_id=550,
            title='Fight Club',
            overview='An insomniac office worker and a devil-may-care soapmaker form an underground fight club.',
            release_date='1999-10-15',
            popularity=26.5,
            vote_average=8.4,
            vote_count=15000
        )
        self.client.force_authenticate(user=self.user)
    
    def test_rate_movie(self):
        """Test rating a movie."""
        data = {'rating': 9, 'review': 'Great movie!'}
        response = self.client.post(f'/api/movies/{self.movie.id}/rate/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MovieRating.objects.filter(user=self.user, movie=self.movie).exists())
    
    def test_update_rating(self):
        """Test updating a movie rating."""
        MovieRating.objects.create(user=self.user, movie=self.movie, rating=7)
        data = {'rating': 9, 'review': 'Updated review'}
        response = self.client.put(f'/api/movies/{self.movie.id}/rate/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        rating = MovieRating.objects.get(user=self.user, movie=self.movie)
        self.assertEqual(rating.rating, 9)
