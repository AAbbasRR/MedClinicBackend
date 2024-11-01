from django.db import IntegrityError, models, transaction
from django.contrib.auth.models import BaseUserManager, AbstractUser, update_last_login
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

from utils.db.models import AbstractSoftDeleteModel
from utils.db.models.soft_delete import AbstractSoftDeleteManager
from utils.exceptions.core import InvalidEmailOrPasswordError, ObjectNotFoundError

from redis_management.redis_manager import RedisManager


class UserEmailManager(models.Manager):
    """
    Manager class for handling user creation and retrieval with email.
    """

    def create_user_with_email(self, email: str, password: str, **kwargs) -> "User":
        """
        Create a new user with the provided email and password.

        Parameters:
        ----------
        email : str
            The email for the new user.
        password : str
            The password for the new user.

        Returns:
        -------
        user : User
            The created user object.

        Raises:
        ------
        ValueError
            If the email or password is not provided.
        """
        if not email:
            raise ValueError("The Email field must be set")
        if not password:
            raise ValueError("The Password field must be set")

        try:
            with transaction.atomic():
                email = self.normalize_email(email)
                user = self.model(email=email, **kwargs)
                user.set_password(password)
                user.save(using=self._db)
                user.username = f"user_{user.pk}"
                user.save()
                return user
        except IntegrityError as e:
            self.handle_existing_user_with_email(email)
            return self.create_user_with_email(email, password, **kwargs)

    def handle_existing_user_with_email(self, email: str) -> bool:
        """
        Handle cases where a user with the given email already exists.

        Parameters:
        ----------
        email : str
            The email of the existing user.
        """
        try:
            user_with_email = self.get(email=self.normalize_email(email))
            if not user_with_email.is_active:
                user_with_email.delete()
                return True
        except self.model.DoesNotExist:
            return True

    def find_by_email(self, email: str) -> "User":
        """
        Find a user by their email.

        Parameters:
        ----------
        email : str
            The email of the user to find.

        Returns:
        -------
        user : User
            The user object.

        Raises:
        ------
        ObjectNotFoundError
            If the user with the given email does not exist.
        """
        try:
            return self.get(email=self.normalize_email(email))
        except self.model.DoesNotExist:
            raise ObjectNotFoundError()

    def list_email_verified(self) -> models.QuerySet:
        """
        List all users with verified emails.

        Returns:
        -------
        QuerySet
            A queryset of users with verified emails.
        """
        return self.filter(email_is_verified=True)


class UserManager(
    BaseUserManager,
    UserEmailManager,
    AbstractSoftDeleteManager,
):
    """
    User manager combining mobile number and email management functionalities.
    """

    def normalize_email(self, email: str) -> str:
        """
        Normalize the email address by converting it to lowercase.

        Parameters:
        ----------
        email : str
            The email to normalize.

        Returns:
        -------
        str
            The normalized email.
        """
        email = super().normalize_email(email)
        return email.lower()

    def create_user(self, email, password, **kwargs) -> "User":
        """
        Create a new user with either an email.

        Returns:
        -------
        user : User
            The created user object.
        """
        return self.create_user_with_email(email, password, **kwargs)

    def authenticate_user(
        self, email: str = None, password: str = None, *args, **kwargs
    ) -> "User":
        """
        Authenticate a user with the given email and password.

        Returns:
        -------
        user : User
            The authenticated user object.

        Raises:
        ------
        InvalidEmailOrPasswordError
            If the user does not exist or the password is incorrect.
        """
        try:
            user_obj = self.get(email=self.normalize_email(email), **kwargs)
            if user_obj.check_password(password):
                return user_obj
            else:
                raise InvalidEmailOrPasswordError()
        except self.model.DoesNotExist:
            raise InvalidEmailOrPasswordError()

    def find_by_email(self, email: str) -> "User":
        """
        Find a user by their email.

        Parameters:
        ----------
        email : str
            The email of the user to find.

        Returns:
        -------
        user : User
            The user object.

        Raises:
        ------
        ObjectNotFoundError
            If the user with the given email does not exist.
        """
        try:
            return self.get(email=self.normalize_email(email))
        except self.model.DoesNotExist:
            raise ObjectNotFoundError()


# noinspection DuplicatedCode
class UserEmail(models.Model):
    """
    Abstract base class for user models with email fields.

    Attributes:
    ----------
    email : str
        The email address of the user.
    email_is_verified : bool
        Indicates if the user's email is verified.
    """

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_deleted=False),
                name="unique_email_if_not_delete",
            ),
        ]

    email = models.EmailField(verbose_name=_("Email Address"))


class User(UserEmail, AbstractUser, AbstractSoftDeleteModel):
    """
    Custom User model combining email and mobile number functionalities, extending AbstractUser.
    """

    # Removing the default first_name, last_name fields from AbstractUser
    class Meta(
        UserEmail.Meta,
        AbstractUser.Meta,
        AbstractSoftDeleteModel.Meta,
    ):
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        constraints = [
            models.UniqueConstraint(
                fields=["email"],
                condition=models.Q(is_deleted=False),
                name="unique_email_if_not_delete",
            ),
        ]

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Is Active"),
    )

    objects = UserManager()

    def __str__(self) -> str:
        """
        String representation of the User object.

        Returns:
        -------
        str
            String representation of the user.
        """
        return f"{self.pk} {self.email}"

    def formatted_last_login(self) -> str:
        """
        Returns the last login time formatted according to DATE_INPUT_FORMAT and TIME_INPUT_FORMAT.

        Returns:
        -------
        str
            Formatted last login time.
        """
        if self.last_login:
            return self.last_login.strftime(
                f"{settings.DATE_INPUT_FORMAT} {settings.TIME_INPUT_FORMAT}"
            )

    def formatted_date_joined(self) -> str:
        """
        Returns the date joined time formatted according to DATE_INPUT_FORMAT and TIME_INPUT_FORMAT.

        Returns:
        -------
        str
            Formatted date joined time.
        """
        return self.date_joined.strftime(
            f"{settings.DATE_INPUT_FORMAT} {settings.TIME_INPUT_FORMAT}"
        )

    def activate(self) -> "User":
        """
        Activates the user account after email validation.

        Returns:
        -------
        self : User
            The updated user object.
        """
        with transaction.atomic():
            self.is_active = True
            self.save()
        return self

    def set_last_login(self) -> "User":
        update_last_login(None, self)
        return self

    def change_password(self, new_pass: str) -> "User":
        with transaction.atomic():
            self.set_password(new_pass)
            self.save()
        return self

    def create_new_token(self) -> dict:
        refresh_token = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
        }

    def user_info(self) -> dict:
        user_info = {
            "email": self.email,
            "date_joined": self.formatted_date_joined(),
            "last_login": self.formatted_last_login(),
            "full_name": self.get_full_name(),
        }

        return user_info

    def user_login_detail(self) -> dict:
        """
        Returns detailed information for user login, including JWT token.

        Returns:
        -------
        dict
            A dictionary containing the user information and JWT token.
        """
        user_info = self.user_info()
        user_info.update({"token": self.create_new_token()})
        return user_info
