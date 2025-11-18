from rest_framework import serializers
from .models import Movie, UserFavoriteMovie, MovieRating


class MovieSerializer(serializers.ModelSerializer):
    """Serializer for Movie model."""
    poster_url = serializers.SerializerMethodField()
    backdrop_url = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'overview', 'release_date',
            'poster_path', 'poster_url', 'backdrop_path', 'backdrop_url',
            'popularity', 'vote_average', 'vote_count', 'original_language',
            'genre_ids', 'is_favorite', 'user_rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_poster_url(self, obj):
        """Generate full poster URL."""
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None
    
    def get_backdrop_url(self, obj):
        """Generate full backdrop URL."""
        if obj.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280{obj.backdrop_path}"
        return None
    
    def get_is_favorite(self, obj):
        """Check if movie is in user's favorites."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserFavoriteMovie.objects.filter(
                user=request.user,
                movie=obj
            ).exists()
        return False
    
    def get_user_rating(self, obj):
        """Get user's rating for the movie."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = MovieRating.objects.filter(
                user=request.user,
                movie=obj
            ).first()
            if rating:
                return {
                    'rating': rating.rating,
                    'review': rating.review,
                    'created_at': rating.created_at
                }
        return None


class MovieDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for Movie model."""
    poster_url = serializers.SerializerMethodField()
    backdrop_url = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()
    user_rating = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = [
            'id', 'tmdb_id', 'title', 'overview', 'release_date',
            'poster_path', 'poster_url', 'backdrop_path', 'backdrop_url',
            'popularity', 'vote_average', 'vote_count', 'original_language',
            'genre_ids', 'is_favorite', 'user_rating', 'average_rating',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_poster_url(self, obj):
        """Generate full poster URL."""
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w500{obj.poster_path}"
        return None
    
    def get_backdrop_url(self, obj):
        """Generate full backdrop URL."""
        if obj.backdrop_path:
            return f"https://image.tmdb.org/t/p/w1280{obj.backdrop_path}"
        return None
    
    def get_is_favorite(self, obj):
        """Check if movie is in user's favorites."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return UserFavoriteMovie.objects.filter(
                user=request.user,
                movie=obj
            ).exists()
        return False
    
    def get_user_rating(self, obj):
        """Get user's rating for the movie."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            rating = MovieRating.objects.filter(
                user=request.user,
                movie=obj
            ).first()
            if rating:
                return {
                    'rating': rating.rating,
                    'review': rating.review,
                    'created_at': rating.created_at
                }
        return None
    
    def get_average_rating(self, obj):
        """Get average rating from all users."""
        ratings = MovieRating.objects.filter(movie=obj)
        if ratings.exists():
            avg = sum(r.rating for r in ratings) / ratings.count()
            return round(avg, 2)
        return None


class UserFavoriteMovieSerializer(serializers.ModelSerializer):
    """Serializer for UserFavoriteMovie model."""
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = UserFavoriteMovie
        fields = ['id', 'movie', 'created_at']
        read_only_fields = ['id', 'created_at']


class MovieRatingSerializer(serializers.ModelSerializer):
    """Serializer for MovieRating model."""
    movie = MovieSerializer(read_only=True)
    
    class Meta:
        model = MovieRating
        fields = ['id', 'movie', 'rating', 'review', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MovieRatingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating movie ratings."""
    
    class Meta:
        model = MovieRating
        fields = ['rating', 'review']
