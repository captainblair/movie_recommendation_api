"""
Custom permission classes for the API.
"""

from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only read.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user


class IsAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Allow any access to safe methods.
    Require authentication for write methods.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAdmin(permissions.BasePermission):
    """
    Allow access only to admin users.
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Allow any access to safe methods.
    Require admin for write methods.
    """
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
