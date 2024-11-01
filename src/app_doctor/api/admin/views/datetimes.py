from app_doctor.api.admin.serializers.datetimes import (
    AdminDoctorDateTimeModelSerializer,
)
from app_doctor.models import DoctorDateTimeModel
from app_doctor.filters.datetimes import DoctorsListFilter

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminDoctorDateTimesListCreateAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminDoctorDateTimeModelSerializer
    queryset = DoctorDateTimeModel.objects.all().order_by("day_of_week", "time")
    filterset_class = DoctorsListFilter


class AdminDoctorDateTimesUpdateDeleteAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminDoctorDateTimeModelSerializer
    queryset = DoctorDateTimeModel.objects.all()
    object_name = "Doctor Datetime"
