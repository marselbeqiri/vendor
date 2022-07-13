import logging

from rest_framework.pagination import PageNumberPagination

logger = logging.getLogger(__name__)


class PageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100
