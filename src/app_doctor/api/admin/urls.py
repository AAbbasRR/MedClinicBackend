from django.urls import path

from .views import *

app_name = "app_doctor_admin"
urlpatterns = [
    # doctor
    path(
        "list-create/",
        AdminDoctorListCreateAPIView.as_view(),
        name="list_create_doctor",
    ),
    path(
        "update-delete/",
        AdminDoctorUpdateDeleteAPIView.as_view(),
        name="update_delete_doctor",
    ),
    # datetime
    path(
        "datetime/list-create/",
        AdminDoctorDateTimesListCreateAPIView.as_view(),
        name="list_create_doctor_datetime",
    ),
    path(
        "datetime/update-delete/",
        AdminDoctorDateTimesUpdateDeleteAPIView.as_view(),
        name="update_delete_doctor_datetime",
    ),
]
