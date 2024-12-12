from app_doctor.api.public.serializers.datetimes import (
    UsersDoctorDateTimeModelSerializer,
)
from app_doctor.models import DoctorDateTimeModel
from app_doctor.filters.datetimes import DoctorsListFilter

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import AllowAnyPermission


class UsersDoctorDateTimesListAPIView(generics.CustomListAPIView):
    permission_classes = [AllowAnyPermission]
    versioning = BaseVersioning
    serializer_class = UsersDoctorDateTimeModelSerializer
    queryset = DoctorDateTimeModel.objects.filter(is_active=True).order_by(
        "date", "time"
    )
    filterset_class = DoctorsListFilter
