from django_filters import FilterSet, DateTimeFromToRangeFilter

from app_reservation.models import ReservationModel


class ReservationListFilter(FilterSet):
    created_at = DateTimeFromToRangeFilter(field_name="created_at")

    class Meta:
        model = ReservationModel
        fields = ["doctor", "date", "time", "created_at"]
