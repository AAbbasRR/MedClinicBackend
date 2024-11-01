from rest_framework import serializers

from utils.serializers import CustomSerializer
from utils.base_errors import BaseErrors
from utils.exceptions.rest import OldPasswordIsIncorrectException


class UserChangePasswordSerializer(CustomSerializer):
    old_password = serializers.CharField(
        required=True, write_only=True, allow_null=True
    )
    password = serializers.CharField(required=True, write_only=True)
    re_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        old_password = attrs.pop("old_password", None)
        password = attrs.get("password")
        re_password = attrs.pop("re_password")

        if password != re_password:
            raise serializers.ValidationError(
                {
                    "password": BaseErrors.passwords_do_not_match,
                    "re_password": BaseErrors.passwords_do_not_match,
                }
            )

        if not self.user.check_password(old_password):
            raise OldPasswordIsIncorrectException()
        self.user.change_password(password)

        return {"detail": BaseErrors.password_successfully_changed}
