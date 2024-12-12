from rest_framework import serializers

from django.utils.timezone import make_aware

from app_doctor.models import DoctorDateTimeModel
from app_reservation.models import ReservationModel

from utils.serializers import CustomModelSerializer

from datetime import datetime, timedelta
import jdatetime


class UsersDoctorDateTimeModelSerializer(CustomModelSerializer):
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = DoctorDateTimeModel
        fields = ("id", "doctor", "date", "time", "is_active")

    def get_is_active(self, obj):
        reservations_exist = ReservationModel.objects.filter(
            doctor=obj.doctor, date=obj.date, time=obj.time
        ).exists()
        return not reservations_exist
