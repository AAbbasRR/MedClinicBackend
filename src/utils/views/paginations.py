from rest_framework import pagination
from rest_framework.response import Response


class BasePagination(pagination.PageNumberPagination):
    """
    Custom pagination class that extends `PageNumberPagination` to provide
    additional metadata about the paginated response.
    """

    page_size = 15
    page_size_query_param = "page_size"

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate the queryset and store additional information for response.

        Parameters:
        ----------
        queryset : QuerySet
            The queryset to paginate.
        request : Request
            The HTTP request object.
        view : View, optional
            The view that is calling this method (default is None).

        Returns:
        -------
        QuerySet
            The paginated queryset.
        """
        # Store the total count of the queryset to avoid multiple counts
        self._count = queryset.count()
        self.response_items = {"count_all": self._count}
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """
        Return a paginated response with additional metadata.

        Parameters:
        ----------
        data : list
            The data to include in the response.

        Returns:
        -------
        Response
            A Response object containing the paginated data and additional metadata.
        """
        response = {"total_pages": self.page.paginator.num_pages, "results": data}
        response.update(self.response_items)
        return Response(response)
