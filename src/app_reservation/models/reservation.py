from django.db import models
from django.utils.translation import gettext_lazy as _

from app_doctor.models.doctors import Doctor

from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel


class Reservation(AbstractDateModel, AbstractSoftDeleteModel):
    class Meta(AbstractDateModel.Meta, AbstractSoftDeleteModel.Meta):
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="doctor_reservs",
        verbose_name=_("Doctor"),
    )
    year = models.IntegerField(verbose_name=_("Year"))
    month = models.CharField(max_length=32, verbose_name=_("Month"))
    date = models.IntegerField(verbose_name=_("Date"))
    day_of_week = models.CharField(max_length=64, verbose_name=_("Day of week"))
    time = models.TimeField(verbose_name=_("Start time"))
    first_name = models.CharField(max_length=128, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=128, verbose_name=_("Last Name"))
    national_code = models.CharField(max_length=64, verbose_name=_("National code"))
    mobile_number = models.CharField(max_length=64, verbose_name=_("Mobile number"))

    def __str__(self):
        return f"{self.year}/{self.month}/{self.date} | {self.time} | {self.first_name} {self.last_name}"
