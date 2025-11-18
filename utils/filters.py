"""
Custom filter classes for the API.
"""

from rest_framework import filters
from django_filters import rest_framework as django_filters
from apps.movies.models import Movie


class MovieFilter(django_filters.FilterSet):
    """Filter for Movie model."""
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Movie title contains'
    )
    release_year = django_filters.NumberFilter(
        field_name='release_date',
        method='filter_release_year',
        label='Release year'
    )
    min_rating = django_filters.NumberFilter(
        field_name='vote_average',
        lookup_expr='gte',
        label='Minimum rating'
    )
    max_rating = django_filters.NumberFilter(
        field_name='vote_average',
        lookup_expr='lte',
        label='Maximum rating'
    )
    min_popularity = django_filters.NumberFilter(
        field_name='popularity',
        lookup_expr='gte',
        label='Minimum popularity'
    )
    
    class Meta:
        model = Movie
        fields = ['title', 'release_year', 'min_rating', 'max_rating', 'min_popularity']
    
    def filter_release_year(self, queryset, name, value):
        """Filter movies by release year."""
        return queryset.filter(release_date__year=value)


class MovieSearchFilter(filters.SearchFilter):
    """Custom search filter for movies."""
    search_param = 'q'
    search_fields = ['title', 'overview', 'original_language']
