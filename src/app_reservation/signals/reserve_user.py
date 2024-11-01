from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from app_reservation.models import ReservationModel
import requests


@receiver(post_save, sender=ReservationModel)
def create_reserve_handler(sender, instance, created, **kwargs):
    if created:
        requests.post(
            "https://api2.ippanel.com/api/v1/sms/pattern/normal/send",
            headers={
                "Content-Type": "application/json",
                "apikey": settings.MEDIANA_API_KEY,
            },
            json={
                "code": "jws0y7pujza1twg",
                "sender": "+983000505",
                "recipient": instance.mobile_number,
                "variable": {
                    "full_name": f"{instance.first_name} {instance.last_name}",
                    "doctor_name": f"{instance.doctor.name}({instance.doctor.field})",
                    "time": str(instance.time),
                    "date": f"{instance.day_of_week} {instance.date} {instance.month} ماه {instance.year}",
                },
            },
        )
