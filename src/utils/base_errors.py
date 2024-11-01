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
    invalid_mobile_number_or_email_format = _("Invalid Mobile Number Or Email Format")
    user_dont_have_forget_password_permission = _(
        "You Do Not Have Access To Change The Password, Please Try Again First Step."
    )
    user_account_not_active = _("User Account Not Active.")
    user_account_is_active = _("User Account Is Active.")
    old_password_is_incorrect = _("Old Password Is Incorrect.")
    invalid_otp_code = _("Invalid OTP Code, Please Try Again.")
    too_much_effort = _(
        "Too Much Effort. You Are Not Allowed To Send Request Minutes, Please Try Again Later"
    )
    cannot_request_to_send_message = _("cannot request to send message")
    your_account_is_locked = _("Your Account Is Locked, Please Try Again Later.")

    # Utils db
    invalid_mobile_number_format = _("Invalid Mobile Number Format.")
    invalid_email_format = _("Invalid Email Format")
    unique_field = _("This Field Already Exists.")

    # permissions
    user_have_verified_mobile_number = _("You Have Verified Mobile Number.")
    user_have_verified_email = _("You Have Verified Email.")
    user_do_not_have_verified_email = _("You Dont Have Verified Email.")
    user_profile_dont_confirmed = _("You Dont Confirmed Profile.")

    # Global errors
    parameter_is_required = _("parameter {param_name} is required.")
    object_not_found = _("{object} Not Found.")
    invalid_field_value = _("Invalid Value.")
    minimum_order_must_value = _("The Minimum Order Amount Must Be {value}")
    you_dont_have_permission_for_this_request = _(
        "You Don't Have Permission For This Request."
    )
    the_maximum_value_should_be_amount = _("The Maximum Value Should be {amount}.")
    filter_date_difference_should_not_more_than_30_days = _(
        "The difference from date to date should not be more than 30 days."
    )
    field_exists = _("Field {field_name} Exists.")
    object_do_not_have_attribute = _("{object} Do Not Have {attribute}")
    user_max_limit_subs_is_full = _("The User {full_name} Max Subs Is Full.")
    notification_title = _("Your {model_name} is {status}")
    description_is = _("Description: {description}")
    user_cant_submit_order_more_than_maximum_rank_amount = _(
        "User Cant Submit Order More Than Max Rank Amount {max_amount}."
    )

    # wallet
    balance_not_enough = _("Balance Not Enough")

    # withdraw
    bank_account_not_confirmed = _("Bank Account Not Confirmed")
    withdrawal_minimum_amount = _("Minimum Withdrawal Amount is {amount}")

    # deposit
    error_in_payment_gateway = _("Problem In The Payment Gateway System")
    deposit_failed = _("Deposit Failed")
    invalid_status_value = _("Invalid Status Value [OK, NOK]")
    payment_time_expired = _("Deposit Failed, Payment Time Expired")
    the_amount_may_not_be_greater_than_1000000000 = _(
        "The Amount May Not Be Greater Than 100000000"
    )

    # ticket
    ticket_closed = _("This ticket is already closed.")
    admin_and_ticket_requester_cannot_be_the_same = _(
        "Admin And Ticket Requester Cannot Be The Same"
    )

    # products
    maximum_depth_parent_child_relationship = _(
        "The Category Cannot Be More Than {depth} Layers"
    )

    # cart
    product_inventory_not_enough = _("Product Inventory Not Enough")

    # order
    your_cart_has_empty = _("Your Cart Has Empty")

    # customer
    cant_delete_active_customer = _("You Can't Delete Active Customer")
    product_order_count_not_enough = _("Product Order Count Not Enough")

    # position
    max_create_sub = _("You Cant Create Sub, Your Max Sub is Full ({max_create}).")
    invalid_heads_items = _("Invalid Heads Items.")
    this_field_value_already_exists = _("This Field Already Exists.")
    the_user_heads_more_than_limit = _("User Heads Too More Than Position Limit.")
    the_user_heads_are_not_suitable_for_its_position = _(
        "The User's Heads Are Not Suitable for its Position."
    )
    user_cant_be_referral = _(
        "Your representative does not have the ability to be a representative"
    )
    referral_income_from_friends = _("Your referral income from friends")
    cant_cancell_definite_order = _("Cant Cancell Definite Order")
    cant_cancell_delivered_or_returned_order = _(
        "Cant Cancell Delivered Or Returned Order"
    )

    # service market
    service_or_market_is_not_active = _("Service Or Market Is Not Active")
