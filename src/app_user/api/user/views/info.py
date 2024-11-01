from rest_framework import response

from utils.views import generics
from utils.views.permissions import IsAuthenticatedPermission
from utils.views.versioning import BaseVersioning


class UserInfoAPIView(generics.CustomGenericGetAPIView):
    permission_classes = [IsAuthenticatedPermission]
    versioning_class = BaseVersioning

    def get(self, *args, **kwargs):
        return response.Response(self.request.user.user_info())
