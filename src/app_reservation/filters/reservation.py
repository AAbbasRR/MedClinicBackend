from django_filters import FilterSet

from app_reservation.models import ReservationModel


class ReservationListFilter(FilterSet):
    class Meta:
        model = ReservationModel
        fields = ["doctor", "day_of_week"]
