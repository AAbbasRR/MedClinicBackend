from rest_framework import serializers

from app_user.models import UserModel

from utils.serializers import CustomModelSerializer
from utils.exceptions.core import InvalidEmailOrPasswordError
from utils.exceptions.rest import InvalidEmailOrPasswordException


class UserLoginSerializer(CustomModelSerializer):
    """
    Serializer for user login. Handles both email/password.

    Attributes:
    ----------
    email : EmailField
        Email of the user.
    """

    email = serializers.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ("email", "password")
        extra_kwargs = {"password": {"required": True}}

    def validate(self, attrs):
        return self._validate_with_email_password(attrs)

    def _validate_with_email_password(self, attrs):
        """
        Validates and authenticates the user using email and password.

        Parameters:
        ----------
        attrs : dict
            The input data for authentication.

        Returns:
        -------
        UserModel
            The authenticated user.

        Raises:
        ------
        UserAccountIsNotActiveException
            If the user's account is not active.
        InvalidEmailOrPasswordException
            If the username or password is invalid.
        """
        try:
            user_obj = UserModel.objects.authenticate_user(**attrs)
            user_obj.set_last_login()
            return user_obj.user_login_detail()
        except InvalidEmailOrPasswordError:
            raise InvalidEmailOrPasswordException()
