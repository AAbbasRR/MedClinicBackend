from rest_framework import serializers

from app_reservation.models import ReservationModel

from utils.serializers import CustomModelSerializer


class AdminReservationSerializer(CustomModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = ReservationModel
        fields = (
            "id",
            "doctor",
            "year",
            "month",
            "date",
            "day_of_week",
            "time",
            "first_name",
            "last_name",
            "mobile_number",
            "national_code",
        )

    def get_doctor(self, obj):
        return {
            "name": obj.doctor.name,
            "field": obj.doctor.field,
        }
