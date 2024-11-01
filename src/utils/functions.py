def get_client_ip(request):
    """
    Extracts the real client IP address from the request, considering proxies and load balancers.

    Parameters:
    ----------
    request : HttpRequest
        The Django request object.

    Returns:
    -------
    str
        The client IP address.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()  # Take the first IP in the list
    else:
        ip = request.META.get("REMOTE_ADDR", "").strip()
    return ip
