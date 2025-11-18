from django.db import models
from django.conf import settings


class Movie(models.Model):
    """
    Movie model to store movie information from TMDb API.
    """
    tmdb_id = models.IntegerField(unique=True, db_index=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)
    backdrop_path = models.CharField(max_length=255, blank=True, null=True)
    popularity = models.FloatField(default=0.0)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)
    original_language = models.CharField(max_length=10, blank=True, null=True)
    genre_ids = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-popularity']
        indexes = [
            models.Index(fields=['tmdb_id']),
            models.Index(fields=['-popularity']),
            models.Index(fields=['-vote_average']),
        ]
    
    def __str__(self):
        return self.title


class UserFavoriteMovie(models.Model):
    """
    Model to store user's favorite movies.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_movies'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'movie']),
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"


class MovieRating(models.Model):
    """
    Model to store user ratings for movies.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='movie_ratings'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name='user_ratings'
    )
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'movie')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'movie']),
            models.Index(fields=['movie', '-rating']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title} ({self.rating}/10)"
