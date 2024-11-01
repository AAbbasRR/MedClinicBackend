from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class AbstractDateModel(models.Model):
    """
    Abstract base model that includes timestamp fields for creation and last update times.
    """

    class Meta:
        abstract = True
        ordering = ["-created_at"]

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created Time"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated Time"))

    def formatted_created_at(self):
        """
        Returns the created_at timestamp formatted according to DATE_INPUT_FORMAT and TIME_INPUT_FORMAT settings.

        Returns:
        -------
        str
            The formatted created_at timestamp.
        """
        return self.created_at.strftime(
            f"{settings.DATE_INPUT_FORMAT} {settings.TIME_INPUT_FORMAT}"
        )

    def formatted_updated_at(self):
        """
        Returns the updated_at timestamp formatted according to DATE_INPUT_FORMAT and TIME_INPUT_FORMAT settings.

        Returns:
        -------
        str
            The formatted updated_at timestamp.
        """
        return self.updated_at.strftime(
            f"{settings.DATE_INPUT_FORMAT} {settings.TIME_INPUT_FORMAT}"
        )
