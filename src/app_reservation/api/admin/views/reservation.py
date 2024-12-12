from django.http import HttpResponse

from app_reservation.api.admin.serializers.reservation import (
    AdminReservationSerializer,
    AdminReservationExportResource,
    AdminCreateReservationSerializer,
)
from app_reservation.models import ReservationModel
from app_reservation.filters.reservation import ReservationListFilter

from utils.views import generics
from utils.views.versioning import BaseVersioning
from utils.views.paginations import BasePagination
from utils.views.permissions import IsAuthenticatedPermission, IsAdminUserPermission


class AdminReservationListAPIView(generics.CustomListCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminReservationSerializer
    pagination_class = BasePagination
    queryset = ReservationModel.objects.all().order_by("date", "time")
    search_fields = (
        "full_name",
        "doctor__name",
        "doctor__field",
        "mobile_number",
        "date",
    )
    filterset_class = ReservationListFilter


class AdminCreateReservationAPIView(generics.CustomCreateAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning = BaseVersioning
    serializer_class = AdminCreateReservationSerializer


class AdminReservationExportListAPIView(generics.CustomListAPIView):
    permission_classes = [IsAuthenticatedPermission, IsAdminUserPermission]
    versioning_class = BaseVersioning
    serializer_class = AdminReservationSerializer
    queryset = ReservationModel.objects.all().order_by("date", "time")
    search_fields = (
        "full_name",
        "doctor__name",
        "doctor__field",
        "mobile_number",
        "date",
    )
    filterset_class = ReservationListFilter

    def get(self, *args, **kwargs):
        resource_class = AdminReservationExportResource()
        dataset = resource_class.export(self.filter_queryset(self.get_queryset()))

        result = HttpResponse(dataset.xlsx, content_type="text/xlsx")
        result["Content-Disposition"] = 'attachment; filename="export_factors.xlsx"'
        return result
