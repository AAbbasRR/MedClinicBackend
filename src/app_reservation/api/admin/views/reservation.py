from app_reservation.api.admin.serializers.reservation import AdminReservationSerializer
from app_reservation.models import ReservationModel

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.paginations import BasePagination
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminReservationListAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminReservationSerializer
    pagination_class = BasePagination
    queryset = ReservationModel.objects.all().order_by("-created_at")
    search_fields = (
        "first_name",
        "last_name",
        "doctor__name",
        "doctor__field",
        "mobile_number",
        "day_of_week",
        "month",
    )
