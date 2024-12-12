from django.conf import settings

from rest_framework import serializers, exceptions

from app_reservation.models import ReservationModel

from utils.serializers import CustomModelSerializer
from utils.base_errors import BaseErrors

from redis_management.redis_manager import RedisManager
import requests


class UsersReservSendOTPSerializer(CustomModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ("mobile_number",)

    def validate(self, attrs):
        redis_manager = RedisManager(attrs["mobile_number"], "verify_otp_code")
        if not redis_manager.exists():
            otp_code = redis_manager.create_and_set_otp_key()
            response = requests.post(
                "https://api2.ippanel.com/api/v1/sms/pattern/normal/send",
                headers={
                    "Content-Type": "application/json",
                    "apikey": settings.MEDIANA_API_KEY,
                },
                json={
                    "code": "0fsjqt5hmdfmlpg",
                    "sender": "+983000505",
                    "recipient": attrs["mobile_number"],
                    "variable": {"OTP": otp_code},
                },
            )
        return attrs


class UsersReservationSerializer(CustomModelSerializer):
    otp = serializers.CharField(max_length=5, write_only=True, required=True)

    class Meta:
        model = ReservationModel
        fields = (
            "id",
            "doctor",
            "date",
            "time",
            "full_name",
            "mobile_number",
            "otp",
        )

    def validate(self, attrs):
        redis_manager = RedisManager(attrs["mobile_number"], "verify_otp_code")
        is_valid = redis_manager.validate(attrs["otp"])
        if is_valid:
            attrs.pop("otp")
            redis_manager.delete()
            return attrs
        else:
            raise exceptions.ParseError({"otp": BaseErrors.invalid_otp_code})
