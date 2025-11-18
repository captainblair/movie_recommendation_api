from django.contrib import admin
from .models import Movie, UserFavoriteMovie, MovieRating


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Admin interface for Movie model."""
    list_display = ['title', 'tmdb_id', 'release_date', 'popularity', 'vote_average', 'created_at']
    list_filter = ['release_date', 'popularity', 'vote_average', 'created_at']
    search_fields = ['title', 'tmdb_id', 'overview']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('tmdb_id', 'title', 'overview', 'original_language')
        }),
        ('Media', {
            'fields': ('poster_path', 'backdrop_path')
        }),
        ('Ratings', {
            'fields': ('popularity', 'vote_average', 'vote_count')
        }),
        ('Metadata', {
            'fields': ('genre_ids', 'release_date', 'created_at', 'updated_at')
        }),
    )


@admin.register(UserFavoriteMovie)
class UserFavoriteMovieAdmin(admin.ModelAdmin):
    """Admin interface for UserFavoriteMovie model."""
    list_display = ['user', 'movie', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['user__username', 'movie__title']
    readonly_fields = ['created_at']


@admin.register(MovieRating)
class MovieRatingAdmin(admin.ModelAdmin):
    """Admin interface for MovieRating model."""
    list_display = ['user', 'movie', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'user']
    search_fields = ['user__username', 'movie__title', 'review']
    readonly_fields = ['created_at', 'updated_at']
