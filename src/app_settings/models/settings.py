from django.db import models
from django.utils.translation import gettext_lazy as _

from app_doctor.models.doctors import Doctor

from utils.db.models import AbstractDateModel


class Settings(AbstractDateModel):
    class Meta(AbstractDateModel.Meta):
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")

    class TypeOptions(models.TextChoices):
        ACTIVATE_GATEWAY = "activate_gateway", _("Activate Gateway")
        GATEWAY_TOKEN = "gateway_token", _("Gateway Token")
        RESERVE_PRICE = "reserve_price", _("Reserve Price")
        TERMS_CONTENT = "terms_content", _("Terms Content")

    type = models.CharField(
        max_length=16, choices=TypeOptions.choices, unique=True, verbose_name=_("Type")
    )
    value = models.TextField(verbose_name=_("Value"))

    def __str__(self):
        return f"{self.type}"
