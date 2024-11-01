from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.db import fields
from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel


class Doctor(AbstractDateModel, AbstractSoftDeleteModel):
    class Meta(AbstractDateModel.Meta, AbstractSoftDeleteModel.Meta):
        verbose_name = _("Doctor")
        verbose_name_plural = _("Doctors")

    name = models.CharField(max_length=100, verbose_name=_("Name"))
    phone = fields.PhoneField(verbose_name=_("Phone"))
    national_code = models.CharField(max_length=10, verbose_name=_("National Code"))
    address = models.TextField(verbose_name=_("Address"))
    field = models.CharField(max_length=64, verbose_name=_("Field"))

    def __str__(self):
        return f"{self.field}:{self.name} ({self.phone})"
