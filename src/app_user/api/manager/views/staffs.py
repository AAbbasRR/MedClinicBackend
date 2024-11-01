from django.db.models import Value, CharField
from django.db.models.functions import Concat

from app_user.api.manager.serializers.staffs import ManagerUserStaffsSerializer
from app_user.models import UserModel

from utils.views import generics
from utils.views.paginations import BasePagination
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class ManagerUserStaffsListCreateAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    pagination_class = BasePagination
    serializer_class = ManagerUserStaffsSerializer
    search_fields = ["email", "full_name"]

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id).annotate(
            full_name=Concat(
                "first_name",
                Value(" "),
                "last_name",
                output_field=CharField(),
            ),
        )


class ManagerUserStaffsUpdateDeleteAPIView(generics.CustomUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = ManagerUserStaffsSerializer
    object_name = "User"

    def get_queryset(self):
        return UserModel.objects.exclude(id=self.request.user.id)
