import jdatetime


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


def get_jalali_day_of_week(jalali_date_str):
    year, month, day = map(int, jalali_date_str.split("/"))
    date = jdatetime.date(year, month, day)
    days_of_week = [
        "شنبه",
        "یکشنبه",
        "دوشنبه",
        "سه‌شنبه",
        "چهارشنبه",
        "پنج‌شنبه",
        "جمعه",
    ]
    return days_of_week[date.weekday()]
