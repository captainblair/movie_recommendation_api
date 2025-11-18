"""
Utility functions for API responses.
"""

from rest_framework.response import Response
from rest_framework import status


def success_response(data, message=None, status_code=status.HTTP_200_OK):
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        message: Optional success message
        status_code: HTTP status code
    
    Returns:
        Response object
    """
    response_data = {
        'success': True,
        'data': data,
    }
    if message:
        response_data['message'] = message
    
    return Response(response_data, status=status_code)


def error_response(error, message=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Create a standardized error response.
    
    Args:
        error: Error details
        message: Optional error message
        status_code: HTTP status code
    
    Returns:
        Response object
    """
    response_data = {
        'success': False,
        'error': error,
    }
    if message:
        response_data['message'] = message
    
    return Response(response_data, status=status_code)


def paginated_response(data, count, page, total_pages, status_code=status.HTTP_200_OK):
    """
    Create a standardized paginated response.
    
    Args:
        data: Paginated data
        count: Total count of items
        page: Current page number
        total_pages: Total number of pages
        status_code: HTTP status code
    
    Returns:
        Response object
    """
    response_data = {
        'success': True,
        'pagination': {
            'count': count,
            'page': page,
            'total_pages': total_pages,
        },
        'results': data,
    }
    
    return Response(response_data, status=status_code)
