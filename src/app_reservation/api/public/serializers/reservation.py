from django.conf import settings

from rest_framework import serializers, exceptions

from app_reservation.models import ReservationModel
from app_settings.models import SettingsModel, OTPManagerModel

from utils.serializers import CustomModelSerializer
from utils.base_errors import BaseErrors
from utils.functions import create_otp_code

from redis_management.redis_manager import RedisManager
import requests


class UsersReservSendOTPSerializer(CustomModelSerializer):
    class Meta:
        model = ReservationModel
        fields = ("mobile_number",)

    def validate(self, attrs):
        otp_code = create_otp_code(5)
        try:
            settings_for_use_redis = SettingsModel.objects.get(
                type=SettingsModel.TypeOptions.USE_REDIS_CACHE
            )
            if bool(int(settings_for_use_redis.value)):
                self._send_otp_code_with_db(otp_code)
            else:
                self._send_otp_code_with_redis(otp_code, attrs["mobile_number"])
        except SettingsModel.DoesNotExist:
            self._send_otp_code_with_db(otp_code)
        return attrs

    def _send_otp_code_with_redis(self, otp_code, mobile_number):
        redis_manager = RedisManager(mobile_number, "verify_otp_code")
        if not redis_manager.exists():
            redis_manager.create_and_set_otp_key(otp_code=otp_code)
            requests.post(
                "https://api2.ippanel.com/api/v1/sms/pattern/normal/send",
                headers={
                    "Content-Type": "application/json",
                    "apikey": settings.MEDIANA_API_KEY,
                },
                json={
                    "code": settings.SMS_SEND_CODE,
                    "sender": "+983000505",
                    "recipient": mobile_number,
                    "variable": {"OTP": otp_code},
                },
            )

    def _send_otp_code_with_db(self, otp_code, mobile_number):
        otp_object, created = OTPManagerModel.objects.get_or_create(
            mobile_number=mobile_number
        )
        otp_object.otp_code = otp_code
        otp_object.save()


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
        is_valid = False
        try:
            settings_for_use_redis = SettingsModel.objects.get(
                type=SettingsModel.TypeOptions.USE_REDIS_CACHE
            )
            if bool(int(settings_for_use_redis.value)):
                is_valid = self._validate_with_redis(
                    attrs["otp"], attrs["mobile_number"]
                )
            else:
                is_valid = self._validate_with_db(attrs["otp"], attrs["mobile_number"])
        except SettingsModel.DoesNotExist:
            is_valid = self._validate_with_db(attrs["otp"], attrs["mobile_number"])

        if is_valid:
            attrs.pop("otp")
            return attrs
        else:
            raise exceptions.ParseError({"otp": BaseErrors.invalid_otp_code})

    def _validate_with_redis(self, otp_code, mobile_number):
        redis_manager = RedisManager("mobile_number", "verify_otp_code")
        is_valid = redis_manager.validate("otp")
        if is_valid:
            redis_manager.delete()
        return is_valid

    def _validate_with_db(self, otp_code, mobile_number):
        try:
            otp_object = OTPManagerModel.objects.get(mobile_number=mobile_number)
            if otp_object.otp_code == otp_code:
                otp_object.delete()
                return True
            return False
        except OTPManagerModel.DoesNotExist:
            return False
