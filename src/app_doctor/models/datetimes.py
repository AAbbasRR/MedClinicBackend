from datetime import timezone

from django.db import models
from django.utils.translation import gettext_lazy as _

from app_doctor.models.doctors import Doctor

from utils.db.models import AbstractDateModel, AbstractSoftDeleteModel


class DoctorDateTime(AbstractDateModel, AbstractSoftDeleteModel):
    class Meta(AbstractDateModel.Meta, AbstractSoftDeleteModel.Meta):
        verbose_name = _("Doctor DateTime")
        verbose_name_plural = _("Doctor DateTimes")
        unique_together = (("doctor", "date", "time"),)

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="doctor_times",
        verbose_name=_("Doctor"),
    )
    date = models.DateField(verbose_name=_("Date"))
    time = models.TimeField(verbose_name=_("Start time"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))

    def __str__(self):
        return f"{self.doctor} {self.date} {self.time}"
