from django.urls import path

from .views import *

app_name = "app_reservation_admin"
urlpatterns = [
    # doctor
    path(
        "list/",
        AdminReservationListAPIView.as_view(),
        name="list_reservations",
    ),
]
