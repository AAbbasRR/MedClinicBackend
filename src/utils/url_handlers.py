from django.http import (
    HttpResponseServerError,
    HttpResponseNotFound,
    JsonResponse,
)
from .base_errors import BaseErrors


def custom_404_response(request, exception):
    """
    Custom 404 error handler.

    Parameters:
    ----------
    request : HttpRequest
        The HTTP request object.
    exception : Exception
        The exception that triggered the 404 response.

    Returns:
    -------
    HttpResponseNotFound
        A JSON response with a 404 status code and error detail.
    """
    return HttpResponseNotFound(JsonResponse({"detail": BaseErrors.url_not_found}))


def custom_500_response(request):
    """
    Custom 500 error handler.

    Parameters:
    ----------
    request : HttpRequest
        The HTTP request object.

    Returns:
    -------
    HttpResponseServerError
        A JSON response with a 500 status code and error detail.
    """
    return HttpResponseServerError(JsonResponse({"detail": BaseErrors.server_error}))
