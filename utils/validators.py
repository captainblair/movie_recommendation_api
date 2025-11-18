"""
Custom validators for the API.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def validate_email(email):
    """Validate email is unique."""
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError("This email is already registered.")
    return email


def validate_username(username):
    """Validate username is unique and valid."""
    if User.objects.filter(username=username).exists():
        raise serializers.ValidationError("This username is already taken.")
    if len(username) < 3:
        raise serializers.ValidationError("Username must be at least 3 characters long.")
    if not username.isalnum():
        raise serializers.ValidationError("Username can only contain letters and numbers.")
    return username


def validate_rating(rating):
    """Validate movie rating is between 1 and 10."""
    if not isinstance(rating, int) or rating < 1 or rating > 10:
        raise serializers.ValidationError("Rating must be an integer between 1 and 10.")
    return rating


def validate_tmdb_id(tmdb_id):
    """Validate TMDb ID is a positive integer."""
    if not isinstance(tmdb_id, int) or tmdb_id <= 0:
        raise serializers.ValidationError("TMDb ID must be a positive integer.")
    return tmdb_id


def validate_search_query(query):
    """Validate search query."""
    if not query or len(query.strip()) == 0:
        raise serializers.ValidationError("Search query cannot be empty.")
    if len(query) > 100:
        raise serializers.ValidationError("Search query cannot exceed 100 characters.")
    return query
