from app_user.api.user.serializers.change_password import UserChangePasswordSerializer

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import IsAuthenticatedPermission


class UserChangePasswordAPIView(generics.CustomGenericPostAPIView):
    permission_classes = [IsAuthenticatedPermission]
    versioning_class = BaseVersioning
    serializer_class = UserChangePasswordSerializer

    def get_serializable_object(self):
        return self.request.user
