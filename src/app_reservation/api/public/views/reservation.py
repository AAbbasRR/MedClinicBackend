from app_reservation.api.public.serializers.reservation import (
    UsersReservSendOTPSerializer,
    UsersReservationSerializer,
)

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.permissions import AllowAnyPermission


class UsersReservationSendOTPAPIView(generics.CustomGenericPostAPIView):
    permission_classes = [AllowAnyPermission]
    versioning = BaseVersioning
    serializer_class = UsersReservSendOTPSerializer


class UsersReservationCreateAPIView(generics.CustomCreateAPIView):
    permission_classes = [AllowAnyPermission]
    versioning = BaseVersioning
    serializer_class = UsersReservationSerializer
