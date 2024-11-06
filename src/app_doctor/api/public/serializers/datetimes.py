from django.utils.timezone import make_aware

from app_doctor.models import DoctorDateTimeModel
from app_reservation.models import ReservationModel

from utils.serializers import CustomModelSerializer

from datetime import datetime, timedelta
import jdatetime


class UsersDoctorDateTimeModelSerializer(CustomModelSerializer):
    class Meta:
        model = DoctorDateTimeModel
        fields = ("id", "doctor", "day_of_week", "time")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["is_active"] = True

        today_gregorian = make_aware(datetime.now())
        today_jalali = jdatetime.date.fromgregorian(date=today_gregorian.date())
        seven_days_later_jalali = today_jalali + timedelta(days=6)

        if ReservationModel.objects.filter(
            doctor=instance.doctor,
            day_of_week=instance.day_of_week,
            time=instance.time,
            year__gte=today_jalali.year,
            month__gte=today_jalali.month,
            date__range=(today_jalali.day, seven_days_later_jalali.day),
        ).exists():
            representation["is_active"] = False
        return representation
