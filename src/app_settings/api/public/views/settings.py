from app_settings.api.public.serializers.settings import UsersSettingsSerializer
from app_settings.models import SettingsModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import AllowAnyPermission


class UsersSettingsAPIView(generics.CustomListAPIView):
    permission_classes = [AllowAnyPermission]
    versioning = BaseVersioning
    serializer_class = UsersSettingsSerializer
    queryset = SettingsModel.objects.all()
