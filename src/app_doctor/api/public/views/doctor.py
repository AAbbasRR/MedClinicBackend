from app_doctor.api.public.serializers.doctor import UsersDoctorSerializer
from app_doctor.models import DoctorModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import AllowAnyPermission


class UsersDoctorListAPIView(generics.CustomListAPIView):
    permission_classes = [AllowAnyPermission]
    versioning = BaseVersioning
    serializer_class = UsersDoctorSerializer
    queryset = DoctorModel.objects.all()
    search_fields = ["name", "field"]
