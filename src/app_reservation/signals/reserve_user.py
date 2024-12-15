from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from app_reservation.models import ReservationModel

from utils.functions import get_jalali_day_of_week
import requests
import jdatetime


@receiver(post_save, sender=ReservationModel)
def create_reserve_handler(sender, instance, created, **kwargs):
    if created:
        year, month, day = map(int, str(instance.date).split("-"))
        jalali_date = jdatetime.GregorianToJalali(year, month, day)
        requests.post(
            "https://api2.ippanel.com/api/v1/sms/pattern/normal/send",
            headers={
                "Content-Type": "application/json",
                "apikey": settings.MEDIANA_API_KEY,
            },
            json={
                "code": settings.SMS_SEND_INFO,
                "sender": "+983000505",
                "recipient": instance.mobile_number,
                "variable": {
                    "full_name": f"{instance.full_name}",
                    "doctor_name": f"{instance.doctor.name}({instance.doctor.field})",
                    "time": str(instance.time),
                    "date": f"{get_jalali_day_of_week(str(instance.date).replace('-', '/'))} {jalali_date.jyear}/{jalali_date.jmonth}/{jalali_date.jday}",
                },
            },
        )
