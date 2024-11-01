from django_filters import FilterSet

from app_doctor.models import DoctorDateTimeModel


class DoctorsListFilter(FilterSet):
    class Meta:
        model = DoctorDateTimeModel
        fields = ["doctor", "day_of_week"]
