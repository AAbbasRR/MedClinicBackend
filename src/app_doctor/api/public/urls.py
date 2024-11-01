from django.urls import path

from .views import *

app_name = "app_doctor_public"
urlpatterns = [
    # doctor
    path(
        "list/",
        UsersDoctorListAPIView.as_view(),
        name="list_doctor",
    ),
    # datetime
    path(
        "datetime/list/",
        UsersDoctorDateTimesListAPIView.as_view(),
        name="list_doctor_datetime",
    ),
]
