from django.db import models
from django.utils.translation import gettext_lazy as _


class OTPManager(models.Model):
    mobile_number = models.CharField(max_length=15, verbose_name=_("Mobile Number"))
    otp_code = models.CharField(
        max_length=15, verbose_name=_("OTP Code"), null=True, blank=True
    )
