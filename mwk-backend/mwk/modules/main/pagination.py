from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class PageParamAPIPagination(PageNumberPagination):
    """
    Pagination for APIs that uses ?page query parameter.
    Removes unused data such as count of records.
    """

    page_size_query_param = 'size'
    max_page_size = None

    def get_paginated_response(self, data: list[dict]) -> Response:
        """
        Return a paginated response incorporating the page link and the requested results.
        """

        return Response(
            {
                'next': self.get_next_link(),
                'results': data,
            }
        )
