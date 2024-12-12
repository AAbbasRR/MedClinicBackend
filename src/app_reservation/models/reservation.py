from django.db import models
from django.utils.translation import gettext_lazy as _

from app_doctor.models.doctors import Doctor

from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel


class Reservation(AbstractDateModel, AbstractSoftDeleteModel):
    class Meta(AbstractDateModel.Meta, AbstractSoftDeleteModel.Meta):
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        unique_together = (("doctor", "date", "time"),)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="doctor_reservs",
        verbose_name=_("Doctor"),
    )
    date = models.DateField(verbose_name=_("Date"))
    time = models.TimeField(verbose_name=_("Start time"))
    full_name = models.CharField(max_length=256, verbose_name=_("First Name"))
    mobile_number = models.CharField(max_length=64, verbose_name=_("Mobile number"))

    def __str__(self):
        return f"{self.date} | {self.time} | {self.full_name}"
