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
    path(
        "create/",
        AdminCreateReservationAPIView.as_view(),
        name="create_reservations",
    ),
    path(
        "list/export/",
        AdminReservationExportListAPIView.as_view(),
        name="list_export_reservations",
    ),
]
