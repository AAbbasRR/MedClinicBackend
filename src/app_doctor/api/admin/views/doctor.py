from app_doctor.api.admin.serializers.doctor import AdminDoctorSerializer
from app_doctor.models import DoctorModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.paginations import BasePagination
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminDoctorListCreateAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    pagination_class = BasePagination
    serializer_class = AdminDoctorSerializer
    queryset = DoctorModel.objects.all()
    search_fields = ["name", "phone", "national_code", "field"]


class AdminDoctorUpdateDeleteAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminDoctorSerializer
    queryset = DoctorModel.objects.all()
    object_name = "Doctor"
