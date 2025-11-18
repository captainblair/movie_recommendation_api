from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserDetailSerializer
)

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom token obtain view with user information."""
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    
    Provides endpoints for:
    - User registration
    - User profile retrieval and update
    - User list (admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """
        Override permissions based on action.
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'list':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action.
        """
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer
    
    def create(self, request, *args, **kwargs):
        """
        Create a new user (registration).
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                'message': 'User registered successfully',
                'user': serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Get current user profile.
        """
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        Update current user profile.
        """
        serializer = UserDetailSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'message': 'Profile updated successfully',
                'user': serializer.data
            },
            status=status.HTTP_200_OK
        )
