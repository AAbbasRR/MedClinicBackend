from django.utils.translation import gettext_lazy as _

from utils.base_errors import BaseErrors


class InvalidEmailOrPasswordError(Exception):
    def __int__(self, message=BaseErrors.invalid_email_or_password):
        self.message = message
        super().__init__(self.message)


class ObjectNotFoundError(Exception):
    def __int__(self, object_name=""):
        self.message = BaseErrors.change_error_variable(
            "object_not_found", object=_(object_name)
        )
        super().__init__(self.message)
