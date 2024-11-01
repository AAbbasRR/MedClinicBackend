from app_settings.api.admin.serializers.settings import AdminSettingsSerializer
from app_settings.models import SettingsModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminSettingListCreateAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminSettingsSerializer
    queryset = SettingsModel.objects.all()


class AdminSettingUpdateAPIView(generics.CustomUpdateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminSettingsSerializer
    queryset = SettingsModel.objects.all()
    object_name = "Setting"
