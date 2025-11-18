"""
Custom pagination classes for the API.
"""

from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class StandardPagination(PageNumberPagination):
    """Standard pagination for list views."""
    page_size = 10
    page_size_query_param = 'page_size'
    page_size_query_description = 'Number of results to return per page.'
    max_page_size = 100
    page_query_description = 'A page number within the paginated result set.'


class LargePagination(PageNumberPagination):
    """Pagination for large result sets."""
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 500


class SmallPagination(PageNumberPagination):
    """Pagination for small result sets."""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20


class MovieCursorPagination(CursorPagination):
    """Cursor-based pagination for movies."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    ordering = '-created_at'
    template = 'rest_framework/pagination/numbers.html'


class CustomPagination(PageNumberPagination):
    """Custom pagination with enhanced response format."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        """Override to provide custom response format."""
        return Response({
            'pagination': {
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'page_size': self.page_size,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
            },
            'results': data
        })
