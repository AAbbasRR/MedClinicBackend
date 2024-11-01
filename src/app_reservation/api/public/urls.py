from django.urls import path

from .views import *

app_name = "app_reservation_public"
urlpatterns = [
    # reservation
    path(
        "send-otp/",
        UsersReservationSendOTPAPIView.as_view(),
        name="send_otp",
    ),
    path(
        "create/",
        UsersReservationCreateAPIView.as_view(),
        name="create_reserve",
    ),
]
