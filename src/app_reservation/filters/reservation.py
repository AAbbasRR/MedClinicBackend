from django_filters import FilterSet, DateTimeFromToRangeFilter

from app_reservation.models import ReservationModel


class ReservationListFilter(FilterSet):
    date = DateTimeFromToRangeFilter(field_name="date")

    class Meta:
        model = ReservationModel
        fields = ["doctor", "date", "time"]
