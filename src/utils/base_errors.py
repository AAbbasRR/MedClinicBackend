from django.utils.translation import gettext_lazy as _


class BaseErrors:
    """
    Base class for handling error messages in a project.
    Provides methods for dynamic error message generation and retrieval.
    """

    @classmethod
    def change_error_variable(cls, error_name, **kwargs):
        """
        Replace placeholders in the error message with provided keyword arguments.

        Parameters:
        ----------
        error_name : str
            The name of the error attribute in the class.
        kwargs : dict
            A dictionary of placeholders and their corresponding values to replace.

        Returns:
        -------
        str
            The error message with replaced values.
        """
        message = getattr(cls, error_name)
        for key, value in kwargs.items():
            message = message.replace("{%s}" % key, str(value))
        return message

    @classmethod
    def return_error_with_name(cls, error_name):
        """
        Retrieve the error message by its attribute name.

        Parameters:
        ----------
        error_name : str
            The name of the error attribute in the class.

        Returns:
        -------
        str
            The error message.
        """
        return getattr(cls, error_name)

    # Project-specific errors
    url_not_found = _("URL Not Found.")
    server_error = _("Server Error.")

    # Public sign up, login, forget password, change password
    passwords_do_not_match = _("Passwords do not match.")
    password_successfully_changed = _("Password successfully changed.")
    invalid_email_or_password = _("Invalid Email Or Password.")
    old_password_is_incorrect = _("Old Password Is Incorrect.")
    invalid_otp_code = _("Invalid OTP Code, Please Try Again.")

    # Utils db
    invalid_mobile_number_format = _("Invalid Mobile Number Format.")
    invalid_email_format = _("Invalid Email Format")
    unique_field = _("This Field Already Exists.")

    # Global errors
    parameter_is_required = _("parameter {param_name} is required.")
    object_not_found = _("{object} Not Found.")
