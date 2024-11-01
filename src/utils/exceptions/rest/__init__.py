from django.utils.translation import gettext_lazy as _

from rest_framework.exceptions import APIException

from utils.base_errors import BaseErrors


class InvalidEmailOrPasswordException(APIException):
    status_code = 400
    default_detail = BaseErrors.invalid_email_or_password


class NotFoundObjectException(APIException):
    status_code = 404

    def __init__(self, detail=BaseErrors.object_not_found, object_name=None):
        if object_name is not None:
            detail = BaseErrors.change_error_variable(
                "object_not_found", object=_(object_name)
            )
        super().__init__(detail)


class ParameterRequiredException(APIException):
    status_code = 400

    def __init__(self, params=None):
        if params is None:
            params = ["pk"]
        detail = BaseErrors.change_error_variable(
            "parameter_is_required", param_name=" or ".join(params)
        )
        super().__init__(detail)


class OldPasswordIsIncorrectException(APIException):
    status_code = 400

    def __init__(
        self, detail=BaseErrors.old_password_is_incorrect, field_name="old_password"
    ):
        super().__init__(detail={field_name: detail})
