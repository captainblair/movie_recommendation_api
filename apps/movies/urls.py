from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MovieViewSet, FavoriteMovieViewSet, MovieRatingViewSet

router = DefaultRouter()
router.register(r'', MovieViewSet, basename='movie')
router.register(r'favorites', FavoriteMovieViewSet, basename='favorite-movie')
router.register(r'ratings', MovieRatingViewSet, basename='movie-rating')

urlpatterns = [
    path('', include(router.urls)),
]
